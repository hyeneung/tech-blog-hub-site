package utils

import (
	"fmt"
	"time"
)

func UnixTime2Time(unixTime int64) time.Time {
	return time.Unix(unixTime, 0).UTC()
}

func Str2UtcTime(strTime string) (time.Time, error) {
	timeFormats := [...]string{
		time.RFC1123,
		time.RFC1123Z,
		time.RFC822Z,
		time.RFC850,
		time.RFC822,
		time.RFC3339,
		"Mon, 2 Jan 2006 15:04:05 -0700",
	}
	for _, format := range timeFormats {
		t, err := time.Parse(format, strTime)
		if err == nil {
			return t.UTC(), nil
		}
	}
	return time.Time{}, fmt.Errorf("failed to parse time: %s", strTime)
}

func GetRFC3339TimeFormat(pubDate string) string {
	t, err := Str2UtcTime(pubDate)
	if err != nil {
		return ""
	}
	return t.Format(time.RFC3339)
}

func RFC3339TimeToUnixTime(rfc3339 string) (int64, error) {
	t, err := time.Parse(time.RFC3339, rfc3339)
	if err != nil {
		return 0, err
	}
	return t.Unix(), nil
}
