package com.internship.tool.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.header.writers.StaticHeadersWriter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;
import java.util.List;

/**
 * Spring Security Configuration
 * Implements authentication, authorization, CSRF protection, and security headers
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /**
     * Configure security filter chain with authentication and authorization
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                // CSRF Protection
                .csrf()
                    .csrfTokenRepository(org.springframework.security.web.csrf.CookieCsrfTokenRepository.withHttpOnlyFalse())
                    .and()
                
                // HTTP to HTTPS redirect (CRITICAL_001 FIX)
                .requiresChannel()
                    .anyRequest()
                    .requiresSecure()
                    .and()
                
                // Authentication & Authorization (CRITICAL_002 FIX)
                .authorizeRequests()
                    .antMatchers("/api/ai/health").permitAll()
                    .antMatchers("/api/ai/**").hasRole("USER")
                    .antMatchers("/api/admin/**").hasRole("ADMIN")
                    .antMatchers("/actuator/**").hasRole("ADMIN")
                    .anyRequest().authenticated()
                    .and()
                
                // HTTP Basic Auth for API
                .httpBasic()
                    .and()
                
                // Security Headers (MEDIUM_004 FIX)
                .headers()
                    .contentSecurityPolicy("default-src 'self'")
                    .and()
                    .xssProtection()
                    .and()
                    .frameOptions().sameOrigin()
                    .and()
                    .addHeaderWriter(new StaticHeadersWriter("X-Content-Type-Options", "nosniff"))
                    .addHeaderWriter(new StaticHeadersWriter("X-Frame-Options", "SAMEORIGIN"))
                    .addHeaderWriter(new StaticHeadersWriter("X-XSS-Protection", "1; mode=block"))
                    .addHeaderWriter(new StaticHeadersWriter("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload"))
                    .and()
                
                // CORS Configuration
                .cors();
        
        return http.build();
    }

    /**
     * CORS Configuration
     */
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(Arrays.asList("https://localhost:3000", "https://localhost:3001"));
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(Arrays.asList("*"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }

    /**
     * Password encoder for credential hashing
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
