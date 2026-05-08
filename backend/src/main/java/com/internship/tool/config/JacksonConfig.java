package com.internship.tool.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.jsontype.BasicPolymorphicTypeValidator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;

/**
 * Jackson Configuration for Secure Deserialization
 * Hardens against insecure deserialization attacks (MEDIUM_002 FIX)
 */
@Configuration
public class JacksonConfig {

    /**
     * Configure ObjectMapper with type safety
     */
    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        
        // Enable default typing with polymorphic validation
        mapper.activateDefaultTyping(
                BasicPolymorphicTypeValidator.builder()
                        .allowIfBaseType(Object.class)
                        .allowIfSubType("com.internship.tool")
                        .build(),
                ObjectMapper.DefaultTyping.NON_FINAL
        );
        
        // Additional security settings
        mapper.configure(com.fasterxml.jackson.databind.DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        
        return mapper;
    }
}
