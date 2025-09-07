# API Endpoint Summary

> Generated from live OpenAPI schema

## GET /api/v1/applications
- operationId: `list_applications_api_v1_applications_get`
- request body: (none or primitive)
- response: (non-object or none)

## POST /api/v1/applications
- operationId: `create_application_api_v1_applications_post`
- request fields:
  - name: string
  - comments: any?
  - id: string
- response fields:
  - name: string
  - comments: any?
  - id: string
  - configuration_ids: List[string]?
- error status codes: 422

## GET /api/v1/applications/{id}
- operationId: `get_application_api_v1_applications__id__get`
- request body: (none or primitive)
- response fields:
  - name: string
  - comments: any?
  - id: string
  - configuration_ids: List[string]?
- error status codes: 422

## PUT /api/v1/applications/{id}
- operationId: `update_application_api_v1_applications__id__put`
- request fields:
  - name: any?
  - comments: any?
- response fields:
  - name: string
  - comments: any?
  - id: string
  - configuration_ids: List[string]?
- error status codes: 422

## POST /api/v1/configurations
- operationId: `create_configuration_api_v1_configurations_post`
- request fields:
  - name: string
  - comments: any?
  - config: object
  - id: string
  - application_id: string
- response fields:
  - name: string
  - comments: any?
  - config: object
  - id: string
  - application_id: string
- error status codes: 422

## GET /api/v1/configurations/{id}
- operationId: `get_configuration_api_v1_configurations__id__get`
- request body: (none or primitive)
- response fields:
  - name: string
  - comments: any?
  - config: object
  - id: string
  - application_id: string
- error status codes: 422

## PUT /api/v1/configurations/{id}
- operationId: `update_configuration_api_v1_configurations__id__put`
- request fields:
  - name: any?
  - comments: any?
  - config: any?
- response fields:
  - name: string
  - comments: any?
  - config: object
  - id: string
  - application_id: string
- error status codes: 422
