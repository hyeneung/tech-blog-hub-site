package org.datacapstonedesign.backend.util;

import org.slf4j.Logger;

public class CustomLogger {
    private CustomLogger() {
        // Utility class, hide constructor
    }

    public static void logError(Logger logger, String operation, String userId, String errors) {
        logger.error("{} failed. User ID: {}. Errors: {}",
            operation,
            userId,
            errors
        );
    }

    public static void logWarn(Logger logger, String operation, String userId, String details) {
        logger.warn("{} warning. User ID: {}. Details: {}",
            operation,
            userId,
            details
        );
    }
}