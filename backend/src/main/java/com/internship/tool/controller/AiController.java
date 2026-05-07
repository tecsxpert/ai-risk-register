package com.internship.tool.controller;

import com.internship.tool.service.AiServiceClient;
import com.internship.tool.service.dto.AiServiceResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

/**
 * REST controller for AI Service integration endpoints.
 * Delegates to AiServiceClient for communication with Flask backend.
 */
@Slf4j
@RestController
@RequestMapping("/api/ai")
public class AiController {
    
    private final AiServiceClient aiServiceClient;
    
    /**
     * Initialize with AiServiceClient.
     *
     * @param aiServiceClient The AI service client
     */
    @Autowired
    public AiController(AiServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }
    
    /**
     * Health check for AI Service.
     *
     * @return Health status response
     */
    @GetMapping("/health")
    public ResponseEntity<?> healthCheck() {
        log.info("Health check requested");
        AiServiceResponse response = aiServiceClient.checkHealth();
        
        if (response != null) {
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.status(503).body(
                    Map.of("status", "error", "message", "AI Service unavailable")
            );
        }
    }
    
    /**
     * Get AI response for a given prompt.
     *
     * @param request Request containing prompt
     * @return AI response
     */
    @PostMapping("/response")
    public ResponseEntity<?> getAiResponse(@RequestBody Map<String, Object> request) {
        try {
            String prompt = (String) request.get("prompt");
            Boolean parseJson = (Boolean) request.getOrDefault("parseJson", false);
            
            log.info("AI response requested for prompt");
            AiServiceResponse response = aiServiceClient.getAiResponse(prompt, parseJson != null && parseJson);
            
            if (response != null && response.getSuccess() != null && response.getSuccess()) {
                return ResponseEntity.ok(response);
            } else if (response != null) {
                return ResponseEntity.status(500).body(response);
            } else {
                return ResponseEntity.status(503).body(
                        Map.of("status", "error", "message", "Failed to get AI response")
                );
            }
        } catch (Exception e) {
            log.error("Error getting AI response: {}", e.getMessage(), e);
            return ResponseEntity.status(400).body(
                    Map.of("status", "error", "message", e.getMessage())
            );
        }
    }
    
    /**
     * Analyze prompt for security threats.
     *
     * @param request Request containing prompt
     * @return Security analysis response
     */
    @PostMapping("/security-analysis")
    public ResponseEntity<?> analyzeSecurity(@RequestBody Map<String, String> request) {
        try {
            String prompt = request.get("prompt");
            
            log.info("Security analysis requested");
            AiServiceResponse response = aiServiceClient.analyzeSecurity(prompt);
            
            if (response != null) {
                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(503).body(
                        Map.of("status", "error", "message", "Security analysis failed")
                );
            }
        } catch (Exception e) {
            log.error("Error analyzing security: {}", e.getMessage(), e);
            return ResponseEntity.status(400).body(
                    Map.of("status", "error", "message", e.getMessage())
            );
        }
    }
    
    /**
     * Generate risk assessment for a topic.
     *
     * @param request Request containing topic
     * @return Risk assessment response
     */
    @PostMapping("/risk-assessment")
    public ResponseEntity<?> generateRiskAssessment(@RequestBody Map<String, String> request) {
        try {
            String topic = request.get("topic");
            
            log.info("Risk assessment requested for topic");
            AiServiceResponse response = aiServiceClient.generateRiskAssessment(topic);
            
            if (response != null) {
                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(503).body(
                        Map.of("status", "error", "message", "Risk assessment failed")
                );
            }
        } catch (Exception e) {
            log.error("Error generating risk assessment: {}", e.getMessage(), e);
            return ResponseEntity.status(400).body(
                    Map.of("status", "error", "message", e.getMessage())
            );
        }
    }
    
    /**
     * Process batch of prompts.
     *
     * @param request Request containing prompts array
     * @return Batch processing response
     */
    @PostMapping("/batch")
    public ResponseEntity<?> processBatch(@RequestBody Map<String, Object> request) {
        try {
            @SuppressWarnings("unchecked")
            java.util.List<String> promptsList = (java.util.List<String>) request.get("prompts");
            String[] prompts = promptsList != null ? promptsList.toArray(new String[0]) : new String[0];
            
            log.info("Batch processing requested with {} prompts", prompts.length);
            AiServiceResponse response = aiServiceClient.processBatch(prompts);
            
            if (response != null) {
                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(503).body(
                        Map.of("status", "error", "message", "Batch processing failed")
                );
            }
        } catch (Exception e) {
            log.error("Error processing batch: {}", e.getMessage(), e);
            return ResponseEntity.status(400).body(
                    Map.of("status", "error", "message", e.getMessage())
            );
        }
    }
}
