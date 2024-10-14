package utils

import (
	"encoding/json"
	"log"
	"os"
)

var Logger *log.Logger

func init() {
	Logger = log.New(os.Stdout, "", log.Ldate|log.Ltime)
}

func LogRequest(userId string, queryParams map[string]string) {
	logEntry := map[string]interface{}{
		"userId":         userId,
		"allQueryParams": queryParams,
	}

	jsonLog, err := json.Marshal(logEntry)
	if err != nil {
		Logger.Printf("Error marshaling log entry: %v", err)
		return
	}

	Logger.Println(string(jsonLog))
}
