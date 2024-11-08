package utils

import (
	"log/slog"
	"net/http"
	"os"
	"sync"
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

	l.logger = slog.New(
		slog.NewJSONHandler(os.Stdout, nil),
	)
	l.ch = make(chan logMessage, 10)
	go l.processLogs()
}

func (l *logger) processLogs() {
	for msg := range l.ch {
		switch msg.level {
		case slog.LevelError:
			l.logger.Error(msg.message, msg.args...)
			os.Exit(1)
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
