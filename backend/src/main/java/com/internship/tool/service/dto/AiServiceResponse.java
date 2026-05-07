package com.internship.tool.service.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * AI Service response DTO for Flask API responses.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AiServiceResponse {
    
    private String status;
    private String message;
    private Object content;
    private String error;
    private Integer retryCount;
    private Boolean success;
}
