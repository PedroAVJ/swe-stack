package main

import (
	"crypto/sha256"
	"database/sql"
	"os"
	"path/filepath"
	"testing"
	"time"

	waProto "go.mau.fi/whatsmeow/binary/proto"
	"go.mau.fi/whatsmeow/types"
	"go.mau.fi/whatsmeow/types/events"
	"google.golang.org/protobuf/proto"
)

func TestSenderToParticipantResolvesBareStoredLID(t *testing.T) {
	storeDir := t.TempDir()
	t.Setenv("WHATSAPP_MCP_STORE_DIR", storeDir)

	db, err := sql.Open("sqlite3", filepath.Join(storeDir, "whatsapp.db"))
	if err != nil {
		t.Fatalf("sql.Open() error = %v", err)
	}
	defer db.Close()

	if _, err := db.Exec("CREATE TABLE whatsmeow_lid_map (lid TEXT PRIMARY KEY, pn TEXT UNIQUE NOT NULL)"); err != nil {
		t.Fatalf("CREATE TABLE error = %v", err)
	}
	if _, err := db.Exec("INSERT INTO whatsmeow_lid_map (lid, pn) VALUES (?, ?)", "99900123456789", "15551230001"); err != nil {
		t.Fatalf("INSERT error = %v", err)
	}

	if got := senderToParticipant("99900123456789"); got != "99900123456789@lid" {
		t.Fatalf("senderToParticipant() = %q, want LID participant", got)
	}
}

func TestSenderToParticipantFallsBackToPhoneJID(t *testing.T) {
	t.Setenv("WHATSAPP_MCP_STORE_DIR", t.TempDir())

	if got := senderToParticipant("15551230001"); got != "15551230001@s.whatsapp.net" {
		t.Fatalf("senderToParticipant() = %q, want phone participant", got)
	}
}

func TestMessageSenderJIDPreservesGroupLIDParticipant(t *testing.T) {
	sender := types.NewJID("99900123456789", types.HiddenUserServer)
	chat := types.NewJID("120363424447729748", types.GroupServer)

	if got := messageSenderJID(sender, chat); got != "99900123456789@lid" {
		t.Fatalf("messageSenderJID() = %q, want full LID JID", got)
	}
}

func TestMessageSenderJIDFallsBackToDirectChatJID(t *testing.T) {
	chat := types.NewJID("15551230001", types.DefaultUserServer)

	if got := messageSenderJID(types.JID{}, chat); got != "15551230001@s.whatsapp.net" {
		t.Fatalf("messageSenderJID() = %q, want direct chat JID", got)
	}
}

func TestBuildReplyContextPreservesFullParticipantJID(t *testing.T) {
	contextInfo := buildReplyContext(ReplyMetadata{
		MessageID: "3AEE6D27A072B2867813",
		Sender:    "99900123456789@lid",
		Content:   "quoted text",
	})

	if contextInfo == nil {
		t.Fatal("buildReplyContext() returned nil")
	}
	if got := contextInfo.GetParticipant(); got != "99900123456789@lid" {
		t.Fatalf("Participant = %q, want full LID JID", got)
	}
	if got := contextInfo.GetStanzaID(); got != "3AEE6D27A072B2867813" {
		t.Fatalf("StanzaID = %q", got)
	}
}

func TestExtractTextContentReadsMediaCaptions(t *testing.T) {
	tests := []struct {
		name string
		msg  *waProto.Message
		want string
	}{
		{
			name: "conversation text",
			msg: &waProto.Message{
				Conversation: proto.String("plain text"),
			},
			want: "plain text",
		},
		{
			name: "extended text",
			msg: &waProto.Message{
				ExtendedTextMessage: &waProto.ExtendedTextMessage{
					Text: proto.String("rich text"),
				},
			},
			want: "rich text",
		},
		{
			name: "image caption",
			msg: &waProto.Message{
				ImageMessage: &waProto.ImageMessage{
					Caption: proto.String("image caption"),
				},
			},
			want: "image caption",
		},
		{
			name: "video caption",
			msg: &waProto.Message{
				VideoMessage: &waProto.VideoMessage{
					Caption: proto.String("video caption"),
				},
			},
			want: "video caption",
		},
		{
			name: "document caption",
			msg: &waProto.Message{
				DocumentMessage: &waProto.DocumentMessage{
					Caption: proto.String("document caption"),
				},
			},
			want: "document caption",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := extractTextContent(tt.msg); got != tt.want {
				t.Fatalf("extractTextContent() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestBuildMediaFilenameUsesMessageID(t *testing.T) {
	tests := []struct {
		name         string
		mediaType    string
		messageID    string
		originalName string
		want         string
	}{
		{
			name:      "image filename",
			mediaType: "image",
			messageID: "3A7F7B003B26545A2A5C",
			want:      "image_3A7F7B003B26545A2A5C.jpg",
		},
		{
			name:      "video filename",
			mediaType: "video",
			messageID: "ABC123",
			want:      "video_ABC123.mp4",
		},
		{
			name:      "audio filename",
			mediaType: "audio",
			messageID: "ABC:123/456",
			want:      "audio_ABC_123_456.ogg",
		},
		{
			name:         "document keeps provided name",
			mediaType:    "document",
			messageID:    "DOC123",
			originalName: "invoice.pdf",
			want:         "invoice.pdf",
		},
		{
			name:      "document fallback uses message id",
			mediaType: "document",
			messageID: "DOC123",
			want:      "document_DOC123",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := buildMediaFilename(tt.mediaType, tt.messageID, tt.originalName); got != tt.want {
				t.Fatalf("buildMediaFilename() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestResolveDownloadFilenameUsesCanonicalMediaName(t *testing.T) {
	tests := []struct {
		name         string
		mediaType    string
		messageID    string
		storedName   string
		wantFilename string
	}{
		{
			name:         "image ignores stale stored name",
			mediaType:    "image",
			messageID:    "3AB93D8B95628CB5EEE9",
			storedName:   "image_20260330_165202.jpg",
			wantFilename: "image_3AB93D8B95628CB5EEE9.jpg",
		},
		{
			name:         "document keeps provided name",
			mediaType:    "document",
			messageID:    "DOC123",
			storedName:   "invoice.pdf",
			wantFilename: "invoice.pdf",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := resolveDownloadFilename(tt.mediaType, tt.messageID, tt.storedName); got != tt.wantFilename {
				t.Fatalf("resolveDownloadFilename() = %q, want %q", got, tt.wantFilename)
			}
		})
	}
}

func TestFileMatchesStoredSHA256(t *testing.T) {
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "sample.jpg")
	data := []byte("not really a jpeg, but enough for hashing")

	if err := os.WriteFile(filePath, data, 0o644); err != nil {
		t.Fatalf("os.WriteFile() error = %v", err)
	}

	expected := sha256.Sum256(data)
	matches, err := fileMatchesStoredSHA256(filePath, expected[:])
	if err != nil {
		t.Fatalf("fileMatchesStoredSHA256() unexpected error = %v", err)
	}
	if !matches {
		t.Fatalf("fileMatchesStoredSHA256() = false, want true")
	}

	wrong := sha256.Sum256([]byte("different"))
	matches, err = fileMatchesStoredSHA256(filePath, wrong[:])
	if err != nil {
		t.Fatalf("fileMatchesStoredSHA256() unexpected error = %v", err)
	}
	if matches {
		t.Fatalf("fileMatchesStoredSHA256() = true, want false")
	}
}

func TestNormalizeMessageForStorageUsesOriginalIDAndEditedPayload(t *testing.T) {
	editedPayload := &waProto.Message{
		ImageMessage: &waProto.ImageMessage{
			Caption: proto.String("edited caption"),
		},
	}

	evt := &events.Message{
		Info: types.MessageInfo{
			ID:        types.MessageID("EDIT-STANZA-ID"),
			Timestamp: time.Unix(1_700_000_000, 0),
		},
		IsEdit: true,
		Message: &waProto.Message{
			ProtocolMessage: &waProto.ProtocolMessage{
				Type: waProto.ProtocolMessage_MESSAGE_EDIT.Enum(),
				Key: &waProto.MessageKey{
					ID: proto.String("ORIGINAL-ID"),
				},
				EditedMessage: editedPayload,
			},
		},
	}

	gotID, gotMessage := normalizeMessageForStorage(evt)
	if gotID != "ORIGINAL-ID" {
		t.Fatalf("normalizeMessageForStorage() id = %q, want %q", gotID, "ORIGINAL-ID")
	}
	if gotMessage != editedPayload {
		t.Fatalf("normalizeMessageForStorage() message payload was not rewritten to edited content")
	}
	if gotCaption := extractTextContent(gotMessage); gotCaption != "edited caption" {
		t.Fatalf("extractTextContent(normalized) = %q, want %q", gotCaption, "edited caption")
	}
}

func TestNormalizeMessageForStorageLeavesRegularMessagesUntouched(t *testing.T) {
	regular := &waProto.Message{
		Conversation: proto.String("plain text"),
	}
	evt := &events.Message{
		Info: types.MessageInfo{
			ID: types.MessageID("REGULAR-ID"),
		},
		Message: regular,
	}

	gotID, gotMessage := normalizeMessageForStorage(evt)
	if gotID != "REGULAR-ID" {
		t.Fatalf("normalizeMessageForStorage() id = %q, want %q", gotID, "REGULAR-ID")
	}
	if gotMessage != regular {
		t.Fatalf("normalizeMessageForStorage() changed a regular message payload unexpectedly")
	}
}
