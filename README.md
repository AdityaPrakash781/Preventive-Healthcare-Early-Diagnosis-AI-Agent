# Preventive-Healthcare-Early-Diagnosis-AI-Agent

Capabl Workshop AI agent project

Build an autonomous AI agent that continuously collects, analyzes, and interprets health data from wearable devices, generates insights for preventive healthcare, and provides early warning signals for anomalies or risks.

Overview:<br>
*Hybrid architecture: LLM only for unstructured-to-structured conversion and natural summaries; all clinical logic, thresholds, risk scoring, storage, and agent decisions are local/deterministic/traceable.<br>
*Agentic: system is event-driven (ingestion triggers parsing → analysis → action). Human UI is optional — agent acts autonomously but presents results on dashboard and via notifications.<br>
*Data-first: standard internal schema for vitals to support uniform analytics/visualization.
