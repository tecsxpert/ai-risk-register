package com.internship.tool.service;

import com.internship.tool.service.dto.AiServiceResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

/**
 * Client for interacting with the AI Service Flask backend.
 * Handles all REST API calls with proper error handling and timeout management.
 */
@Slf4j
@Service
public class AiServiceClient {
    
    private final RestTemplate restTemplate;
    
    @Value("${ai.service.base-url:http://localhost:5000}")
    private String aiServiceBaseUrl;
    
    /**
     * Initialize AiServiceClient with RestTemplate.
     *
     * @param restTemplate RestTemplate bean with configured timeouts
     */
    @Autowired
    public AiServiceClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
        log.info("AiServiceClient initialized with base URL: {}", aiServiceBaseUrl);
    }
    
    /**
     * Check health status of AI Service.
     *
     * @return AiServiceResponse with health status, or null on error
     */
    public AiServiceResponse checkHealth() {
        try {
            log.info("Calling health check endpoint");
            String url = aiServiceBaseUrl + "/health";
            ResponseEntity<AiServiceResponse> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    null,
                    AiServiceResponse.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                log.info("Health check successful");
                return response.getBody();
            } else {
                log.warn("Health check returned status: {}", response.getStatusCode());
                return null;
            }
        } catch (RestClientException e) {
            log.error("Health check failed: {}", e.getMessage(), e);
            return null;
        } catch (Exception e) {
            log.error("Unexpected error during health check: {}", e.getMessage(), e);
            return null;
        }
    }
    
    /**
     * Send a prompt to the AI Service and get a response.
     *
     * @param prompt The user prompt to send
     * @return AiServiceResponse with AI response, or null on error
     */
    public AiServiceResponse getAiResponse(String prompt) {
        return getAiResponse(prompt, false);
    }
    
    /**
     * Send a prompt to the AI Service and optionally parse response as JSON.
     *
     * @param prompt    The user prompt to send
     * @param parseJson Whether to parse response as JSON
     * @return AiServiceResponse with AI response, or null on error
     */
    public AiServiceResponse getAiResponse(String prompt, boolean parseJson) {
        try {
            if (prompt == null || prompt.trim().isEmpty()) {
                log.warn("Prompt is null or empty");
                return null;
            }
            
            log.info("Sending AI prompt request");
            String url = aiServiceBaseUrl + "/ai/response";
            
            // Create request body
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("prompt", prompt);
            requestBody.put("parseJson", parseJson);
            
            HttpEntity<Map<String, Object>> request = createJsonRequest(requestBody);
            
            ResponseEntity<AiServiceResponse> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    request,
                    AiServiceResponse.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                log.info("AI response received successfully");
                return response.getBody();
            } else {
                log.warn("AI response returned status: {}", response.getStatusCode());
                return null;
            }
        } catch (RestClientException e) {
            log.error("AI response call failed: {}", e.getMessage(), e);
            return null;
        } catch (Exception e) {
            log.error("Unexpected error during AI response call: {}", e.getMessage(), e);
            return null;
        }
    }
    
    /**
     * Analyze a prompt for security threats.
     *
     * @param prompt The prompt to analyze
     * @return AiServiceResponse with analysis results, or null on error
     */
    public AiServiceResponse analyzeSecurity(String prompt) {
        try {
            if (prompt == null || prompt.trim().isEmpty()) {
                log.warn("Prompt is null or empty for security analysis");
                return null;
            }
            
            log.info("Sending security analysis request");
            String url = aiServiceBaseUrl + "/ai/analyze-security";
            
            Map<String, String> requestBody = new HashMap<>();
            requestBody.put("prompt", prompt);
            
            HttpEntity<Map<String, String>> request = createJsonRequest(requestBody);
            
            ResponseEntity<AiServiceResponse> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    request,
                    AiServiceResponse.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                log.info("Security analysis completed successfully");
                return response.getBody();
            } else {
                log.warn("Security analysis returned status: {}", response.getStatusCode());
                return null;
            }
        } catch (RestClientException e) {
            log.error("Security analysis failed: {}", e.getMessage(), e);
            return null;
        } catch (Exception e) {
            log.error("Unexpected error during security analysis: {}", e.getMessage(), e);
            return null;
        }
    }
    
    /**
     * Generate a risk assessment for a given topic.
     *
     * @param topic The topic to assess
     * @return AiServiceResponse with risk assessment, or null on error
     */
    public AiServiceResponse generateRiskAssessment(String topic) {
        try {
            if (topic == null || topic.trim().isEmpty()) {
                log.warn("Topic is null or empty for risk assessment");
                return null;
            }
            
            log.info("Sending risk assessment request for topic: {}", topic);
            String url = aiServiceBaseUrl + "/ai/risk-assessment";
            
            Map<String, String> requestBody = new HashMap<>();
            requestBody.put("topic", topic);
            
            HttpEntity<Map<String, String>> request = createJsonRequest(requestBody);
            
            ResponseEntity<AiServiceResponse> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    request,
                    AiServiceResponse.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                log.info("Risk assessment generated successfully");
                return response.getBody();
            } else {
                log.warn("Risk assessment returned status: {}", response.getStatusCode());
                return null;
            }
        } catch (RestClientException e) {
            log.error("Risk assessment failed: {}", e.getMessage(), e);
            return null;
        } catch (Exception e) {
            log.error("Unexpected error during risk assessment: {}", e.getMessage(), e);
            return null;
        }
    }
    
    /**
     * Send a batch of prompts for processing.
     *
     * @param prompts Array of prompts to process
     * @return AiServiceResponse with batch results, or null on error
     */
    public AiServiceResponse processBatch(String[] prompts) {
        try {
            if (prompts == null || prompts.length == 0) {
                log.warn("Prompts array is null or empty");
                return null;
            }
            
            log.info("Sending batch processing request with {} prompts", prompts.length);
            String url = aiServiceBaseUrl + "/ai/batch";
            
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("prompts", prompts);
            
            HttpEntity<Map<String, Object>> request = createJsonRequest(requestBody);
            
            ResponseEntity<AiServiceResponse> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    request,
                    AiServiceResponse.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                log.info("Batch processing completed successfully");
                return response.getBody();
            } else {
                log.warn("Batch processing returned status: {}", response.getStatusCode());
                return null;
            }
        } catch (RestClientException e) {
            log.error("Batch processing failed: {}", e.getMessage(), e);
            return null;
        } catch (Exception e) {
            log.error("Unexpected error during batch processing: {}", e.getMessage(), e);
            return null;
        }
    }
    
    /**
     * Create an HTTP request with JSON content type and headers.
     *
     * @param body Request body object
     * @return HttpEntity with proper headers
     */
    private <T> HttpEntity<T> createJsonRequest(T body) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("Accept", MediaType.APPLICATION_JSON_VALUE);
        return new HttpEntity<>(body, headers);
    }
    
    /**
     * Set the AI Service base URL (useful for testing).
     *
     * @param url Base URL of the AI Service
     */
    public void setAiServiceBaseUrl(String url) {
        this.aiServiceBaseUrl = url;
        log.info("AI Service base URL updated to: {}", url);
    }
    
    /**
     * Get the current AI Service base URL.
     *
     * @return Current base URL
     */
    public String getAiServiceBaseUrl() {
        return aiServiceBaseUrl;
    }
}
