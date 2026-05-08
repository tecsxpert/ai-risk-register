package com.internship.tool.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;

/**
 * Authentication Configuration
 * Provides in-memory user authentication for API
 */
@Configuration
public class AuthenticationConfig {

    /**
     * Configure in-memory users for API authentication
     */
    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails user = User.builder()
                .username("api_user")
                .password("$2a$10$slYQmyNdGzin7olVN3p5be4DlH.PKZbv5H8KnzzVgXXbVxzy76uDm") // bcrypt of "password123"
                .roles("USER")
                .accountExpired(false)
                .accountLocked(false)
                .credentialsExpired(false)
                .disabled(false)
                .build();

        UserDetails admin = User.builder()
                .username("admin")
                .password("$2a$10$dXJ3SW6G7P50eS3tWQfuA.0Y5v3aPO3m8R8.P4A.7bz5xMpNO46pi") // bcrypt of "admin123"
                .roles("ADMIN", "USER")
                .accountExpired(false)
                .accountLocked(false)
                .credentialsExpired(false)
                .disabled(false)
                .build();

        return new InMemoryUserDetailsManager(user, admin);
    }
}
