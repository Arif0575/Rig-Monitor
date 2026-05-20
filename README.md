# Rig-Monitor

A self-hosted Python telemetry monitoring project running on an Unraid NAS using Docker containers.

The system queries hardware telemetry via JSON APIs, extracts key metrics such as CPU temperature, GPU power draw, and system statistics, and forms the foundation for future AI-assisted monitoring and summarisation workflows.

## Current Features
- Query live telemetry data via JSON endpoints
- Extract CPU and GPU metrics using Python
- Docker-based execution on Unraid
- Structured sensor path parsing
- Foundation for future logging and alerting

## Planned Features
- SQLite telemetry history
- Automated anomaly detection
- Discord notifications
- AI-generated summaries
- Multi-system monitoring
- Long-term telemetry tracking

## Stack
- Python
- Docker
- Unraid
- JSON APIs
- Local AI / LLM experimentation
