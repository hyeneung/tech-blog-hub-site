package utils

import (
	"log"
	"log/slog"
	"net/http"
	"os"
	"sync"
	"time"

	config "crawler/config"

	slogmulti "github.com/samber/slog-multi"
	"gopkg.in/natefinch/lumberjack.v2"
)

type logMessage struct {
	level   slog.Level
	message string
	args    []any
}

type logger struct {
	logger *slog.Logger
	ch     chan logMessage
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
	logFilePath := getLogFilePath()
	lumberjackLogger := &lumberjack.Logger{
		Filename:   logFilePath,
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
	l.ch = make(chan logMessage, 20)
	go l.processLogs()
}

func (l *logger) processLogs() {
	for msg := range l.ch {
		switch msg.level {
		case slog.LevelError:
			l.logger.Error(msg.message, msg.args...)
		case slog.LevelInfo:
			l.logger.Info(msg.message, msg.args...)
		case slog.LevelDebug:
			l.logger.Debug(msg.message, msg.args...)
		}
	}
}
func (l *logger) LogError(message string, args ...any) {
	l.ch <- logMessage{level: slog.LevelError, message: message, args: args}
}

func (l *logger) LogInfo(message string, args ...any) {
	l.ch <- logMessage{level: slog.LevelInfo, message: message, args: args}
}

func (l *logger) LogDebug(message string, args ...any) {
	l.ch <- logMessage{level: slog.LevelDebug, message: message, args: args}
}

func (l *logger) LogWarn(message string, args ...any) {
	l.ch <- logMessage{level: slog.LevelWarn, message: message, args: args}
}

func (l *logger) LogHttpResponseError(resp *http.Response) {
	l.LogError("HTTP response error", slog.Int("Status Code", resp.StatusCode))
}

func (l *logger) LogCrawlerResult(companyName string, totalCount int, successCount uint32) {
	l.LogInfo("Update Done",
		slog.String("crawler", companyName),
		slog.Group("results",
			"newly posted", totalCount,
			"updated", successCount,
		),
	)
}

func (l *logger) Close() {
	close(l.ch)
}

func getLogFilePath() string {
	cfg := config.GetConfigSingletonInstance()
	logFolderPath := cfg.LogFolderPath
	if _, err := os.Stat(logFolderPath); os.IsNotExist(err) {
		err := os.Mkdir(logFolderPath, 0700)
		if err != nil {
			log.Fatal("failed to create log directory: " + err.Error())
		}
	}
	logFileName := time.Now().Format("2006-01-01_15h04m05s") + ".log"
	fileName := logFolderPath + logFileName
	if _, err := os.Stat(fileName); err != nil {
		if _, err := os.Create(fileName); err != nil {
			log.Fatal("failed to create log file: " + err.Error())
		}
	}
	return fileName
}
