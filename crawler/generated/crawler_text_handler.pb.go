// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.34.2
// 	protoc        v5.27.0--rc3
// source: crawler_text_handler.proto

package generated

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type UrlRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Url string `protobuf:"bytes,1,opt,name=url,proto3" json:"url,omitempty"`
}

func (x *UrlRequest) Reset() {
	*x = UrlRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_crawler_text_handler_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *UrlRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*UrlRequest) ProtoMessage() {}

func (x *UrlRequest) ProtoReflect() protoreflect.Message {
	mi := &file_crawler_text_handler_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use UrlRequest.ProtoReflect.Descriptor instead.
func (*UrlRequest) Descriptor() ([]byte, []int) {
	return file_crawler_text_handler_proto_rawDescGZIP(), []int{0}
}

func (x *UrlRequest) GetUrl() string {
	if x != nil {
		return x.Url
	}
	return ""
}

type SummarizedDataResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	SummarizedText string   `protobuf:"bytes,1,opt,name=summarized_text,json=summarizedText,proto3" json:"summarized_text,omitempty"`
	Hashtags       []string `protobuf:"bytes,2,rep,name=hashtags,proto3" json:"hashtags,omitempty"`
}

func (x *SummarizedDataResponse) Reset() {
	*x = SummarizedDataResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_crawler_text_handler_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SummarizedDataResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SummarizedDataResponse) ProtoMessage() {}

func (x *SummarizedDataResponse) ProtoReflect() protoreflect.Message {
	mi := &file_crawler_text_handler_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SummarizedDataResponse.ProtoReflect.Descriptor instead.
func (*SummarizedDataResponse) Descriptor() ([]byte, []int) {
	return file_crawler_text_handler_proto_rawDescGZIP(), []int{1}
}

func (x *SummarizedDataResponse) GetSummarizedText() string {
	if x != nil {
		return x.SummarizedText
	}
	return ""
}

func (x *SummarizedDataResponse) GetHashtags() []string {
	if x != nil {
		return x.Hashtags
	}
	return nil
}

var File_crawler_text_handler_proto protoreflect.FileDescriptor

var file_crawler_text_handler_proto_rawDesc = []byte{
	0x0a, 0x1a, 0x63, 0x72, 0x61, 0x77, 0x6c, 0x65, 0x72, 0x5f, 0x74, 0x65, 0x78, 0x74, 0x5f, 0x68,
	0x61, 0x6e, 0x64, 0x6c, 0x65, 0x72, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x22, 0x1e, 0x0a, 0x0a,
	0x55, 0x72, 0x6c, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x10, 0x0a, 0x03, 0x75, 0x72,
	0x6c, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x03, 0x75, 0x72, 0x6c, 0x22, 0x5d, 0x0a, 0x16,
	0x53, 0x75, 0x6d, 0x6d, 0x61, 0x72, 0x69, 0x7a, 0x65, 0x64, 0x44, 0x61, 0x74, 0x61, 0x52, 0x65,
	0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x27, 0x0a, 0x0f, 0x73, 0x75, 0x6d, 0x6d, 0x61, 0x72,
	0x69, 0x7a, 0x65, 0x64, 0x5f, 0x74, 0x65, 0x78, 0x74, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52,
	0x0e, 0x73, 0x75, 0x6d, 0x6d, 0x61, 0x72, 0x69, 0x7a, 0x65, 0x64, 0x54, 0x65, 0x78, 0x74, 0x12,
	0x1a, 0x0a, 0x08, 0x68, 0x61, 0x73, 0x68, 0x74, 0x61, 0x67, 0x73, 0x18, 0x02, 0x20, 0x03, 0x28,
	0x09, 0x52, 0x08, 0x68, 0x61, 0x73, 0x68, 0x74, 0x61, 0x67, 0x73, 0x32, 0x56, 0x0a, 0x12, 0x43,
	0x72, 0x61, 0x77, 0x6c, 0x65, 0x72, 0x54, 0x65, 0x78, 0x74, 0x48, 0x61, 0x6e, 0x64, 0x6c, 0x65,
	0x72, 0x12, 0x40, 0x0a, 0x12, 0x53, 0x74, 0x72, 0x65, 0x61, 0x6d, 0x55, 0x72, 0x6c, 0x53, 0x75,
	0x6d, 0x6d, 0x61, 0x72, 0x69, 0x65, 0x73, 0x12, 0x0b, 0x2e, 0x55, 0x72, 0x6c, 0x52, 0x65, 0x71,
	0x75, 0x65, 0x73, 0x74, 0x1a, 0x17, 0x2e, 0x53, 0x75, 0x6d, 0x6d, 0x61, 0x72, 0x69, 0x7a, 0x65,
	0x64, 0x44, 0x61, 0x74, 0x61, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x22, 0x00, 0x28,
	0x01, 0x30, 0x01, 0x42, 0x19, 0x5a, 0x17, 0x2e, 0x2e, 0x2f, 0x2e, 0x2e, 0x2f, 0x63, 0x72, 0x61,
	0x77, 0x6c, 0x65, 0x72, 0x2f, 0x67, 0x65, 0x6e, 0x65, 0x72, 0x61, 0x74, 0x65, 0x64, 0x62, 0x06,
	0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_crawler_text_handler_proto_rawDescOnce sync.Once
	file_crawler_text_handler_proto_rawDescData = file_crawler_text_handler_proto_rawDesc
)

func file_crawler_text_handler_proto_rawDescGZIP() []byte {
	file_crawler_text_handler_proto_rawDescOnce.Do(func() {
		file_crawler_text_handler_proto_rawDescData = protoimpl.X.CompressGZIP(file_crawler_text_handler_proto_rawDescData)
	})
	return file_crawler_text_handler_proto_rawDescData
}

var file_crawler_text_handler_proto_msgTypes = make([]protoimpl.MessageInfo, 2)
var file_crawler_text_handler_proto_goTypes = []any{
	(*UrlRequest)(nil),             // 0: UrlRequest
	(*SummarizedDataResponse)(nil), // 1: SummarizedDataResponse
}
var file_crawler_text_handler_proto_depIdxs = []int32{
	0, // 0: CrawlerTextHandler.StreamUrlSummaries:input_type -> UrlRequest
	1, // 1: CrawlerTextHandler.StreamUrlSummaries:output_type -> SummarizedDataResponse
	1, // [1:2] is the sub-list for method output_type
	0, // [0:1] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_crawler_text_handler_proto_init() }
func file_crawler_text_handler_proto_init() {
	if File_crawler_text_handler_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_crawler_text_handler_proto_msgTypes[0].Exporter = func(v any, i int) any {
			switch v := v.(*UrlRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_crawler_text_handler_proto_msgTypes[1].Exporter = func(v any, i int) any {
			switch v := v.(*SummarizedDataResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_crawler_text_handler_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   2,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_crawler_text_handler_proto_goTypes,
		DependencyIndexes: file_crawler_text_handler_proto_depIdxs,
		MessageInfos:      file_crawler_text_handler_proto_msgTypes,
	}.Build()
	File_crawler_text_handler_proto = out.File
	file_crawler_text_handler_proto_rawDesc = nil
	file_crawler_text_handler_proto_goTypes = nil
	file_crawler_text_handler_proto_depIdxs = nil
}
