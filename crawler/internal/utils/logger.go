package utils

import (
	"log"
	"log/slog"
	"net/http"
	"os"
	"sync"
	"time"

	slogmulti "github.com/samber/slog-multi"
	"gopkg.in/natefinch/lumberjack.v2"
)

type logger struct {
	logger *slog.Logger
}

// singleton pattern
var instance *logger
var once sync.Once

func GetLoggerSingletonInstance() *logger {
	once.Do(func() {
		instance = &logger{}
		instance.initLogger()
	})
	return instance
}

func (l *logger) initLogger() {
	lumberjackLogger := &lumberjack.Logger{
		Filename:   getLogFilePath(),
		MaxSize:    20,
		MaxBackups: 5,
		MaxAge:     10,
		Compress:   true,
	}

	l.logger = slog.New(
		slogmulti.Fanout(
			slog.NewJSONHandler(os.Stdout, nil),
			slog.NewJSONHandler(lumberjackLogger, nil),
		),
	)
}

func (l *logger) LogError(message string) {
	l.logger.Error(message)
}

func (l *logger) LogInfo(message string) {
	l.logger.Info(message)
}

func (l *logger) LogDebug(message string) {
	l.logger.Debug(message)
}

func (l *logger) LogHttpResponseError(resp *http.Response) {
	l.logger.Error("HTTP response error", slog.Int("Status Code", resp.StatusCode))
}

func (l *logger) LogCrawlerResult(companyName string, totalCount int, successCount uint32) {
	resultLogger := l.logger.With(
		slog.String("crawler", companyName),
		slog.Group("results",
			"newly posted", totalCount,
			"updated", successCount,
		),
	)
	resultLogger.Info("Update Done")
}

func getLogFilePath() string {
	// logFolderPath := os.Getenv("CRAWLER_LOG_FOLDER_PATH")
	logFolderPath := "./log/"
	if _, err := os.Stat(logFolderPath); os.IsNotExist(err) {
		err := os.Mkdir(logFolderPath, 0700)
		if err != nil {
			log.Fatalln(err.Error())
		}
	}
	logFileName := time.Now().Format("2006-01-01_15h04m05s") + ".log"
	fileName := logFolderPath + logFileName
	if _, err := os.Stat(fileName); err != nil {
		log.Println("creating file", fileName)
		if _, err := os.Create(fileName); err != nil {
			log.Println(err.Error())
		}
	}
	return fileName
}
