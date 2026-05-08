package com.internship.tool.security;

import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.event.AbstractAuthenticationFailureEvent;
import org.springframework.security.authentication.event.AuthenticationSuccessEvent;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Security Event Logger
 * Implements comprehensive security event logging (MEDIUM_003 FIX)
 */
@Component
@Slf4j
public class SecurityEventLogger implements HandlerInterceptor {

    private static final DateTimeFormatter dateFormat = DateTimeFormatter.ISO_DATE_TIME;

    /**
     * Log authentication success events
     */
    public void logAuthenticationSuccess(Authentication auth) {
        log.info("SECURITY_EVENT=AUTH_SUCCESS | timestamp={} | user={} | principal={} | source={}",
                LocalDateTime.now().format(dateFormat),
                auth.getName(),
                auth.getPrincipal().getClass().getSimpleName(),
                getAuthenticationSource(auth));
    }

    /**
     * Log authentication failure events
     */
    public void logAuthenticationFailure(String username, String reason) {
        log.warn("SECURITY_EVENT=AUTH_FAILURE | timestamp={} | user={} | reason={} | severity=MEDIUM",
                LocalDateTime.now().format(dateFormat),
                username,
                reason);
    }

    /**
     * Log authorization failures
     */
    public void logAuthorizationFailure(String user, String endpoint, String requiredRole) {
        log.warn("SECURITY_EVENT=AUTHZ_FAILURE | timestamp={} | user={} | endpoint={} | required_role={} | severity=MEDIUM",
                LocalDateTime.now().format(dateFormat),
                user,
                endpoint,
                requiredRole);
    }

    /**
     * Log sensitive data access
     */
    public void logDataAccess(String user, String endpoint, String dataType) {
        log.info("SECURITY_EVENT=DATA_ACCESS | timestamp={} | user={} | endpoint={} | data_type={}",
                LocalDateTime.now().format(dateFormat),
                user,
                endpoint,
                dataType);
    }

    /**
     * Log security violations (injection attempts, etc)
     */
    public void logSecurityViolation(String user, String endpoint, String violation) {
        log.error("SECURITY_EVENT=VIOLATION | timestamp={} | user={} | endpoint={} | violation={} | severity=HIGH",
                LocalDateTime.now().format(dateFormat),
                user,
                endpoint,
                violation);
    }

    /**
     * Log admin actions
     */
    public void logAdminAction(String admin, String action, String target) {
        log.info("SECURITY_EVENT=ADMIN_ACTION | timestamp={} | admin={} | action={} | target={}",
                LocalDateTime.now().format(dateFormat),
                admin,
                action,
                target);
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String method = request.getMethod();
        String endpoint = request.getRequestURI();
        String ip = getClientIp(request);

        if (isStateChangingOperation(method)) {
            log.debug("SECURITY_EVENT=REQUEST | timestamp={} | method={} | endpoint={} | ip={}",
                    LocalDateTime.now().format(dateFormat),
                    method,
                    endpoint,
                    ip);
        }

        return true;
    }

    private String getAuthenticationSource(Authentication auth) {
        if (auth.getDetails() != null) {
            return auth.getDetails().toString();
        }
        return "UNKNOWN";
    }

    private boolean isStateChangingOperation(String method) {
        return method.equals("POST") || method.equals("PUT") || 
               method.equals("DELETE") || method.equals("PATCH");
    }

    private String getClientIp(HttpServletRequest request) {
        String xForwardedFor = request.getHeader("X-Forwarded-For");
        if (xForwardedFor != null && !xForwardedFor.isEmpty()) {
            return xForwardedFor.split(",")[0].trim();
        }
        return request.getRemoteAddr();
    }
}
