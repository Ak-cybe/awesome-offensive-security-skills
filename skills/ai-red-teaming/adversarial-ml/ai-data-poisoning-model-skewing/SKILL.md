---
name: ai-data-poisoning-model-skewing
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Identify and simulate Data Poisoning attacks aimed at degrading or skewing an AI model's accuracy. 
  This skill focuses on Adversarial Machine Learning concepts where attackers inject malicious or 
  mislabelled data points into training or fine-tuning datasets (e.g., feedback loops) to bias the AI.
domain: cybersecurity
subdomain: ai-red-teaming
category: Adversarial ML
difficulty: advanced
estimated_time: "4-5 hours"
mitre_atlas:
  tactics: [AML.TA0001]
  techniques: [AML.T0043, AML.T0051]
mitre_attack:
  tactics: [TA0001, TA0010]
  techniques: [T1565.003, T1036]
platforms: [ai, machine-learning]
tags: [data-poisoning, adversarial-ml, model-skewing, ai-red-teaming, feedback-loops, availability-attack]
tools: [python, jupyter-notebook]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# AI Data Poisoning (Model Skewing)

## When to Use
- When conducting a red team assessment on an AI system that implements continuous learning, reinforcement learning from human feedback (RLHF), or accepts user-submitted data for future retraining.
- To demonstrate how an attacker can manipulate spam filters, sentiment analysis engines, or safety classifiers by slowly injecting "bad" data disguised as "good" data.

## Workflow

### Phase 1: Identifying the Feedback/Training Loop

Determine if the AI system uses your inputs for retraining. - Are there "Thumbs up/Thumbs down" buttons?
- Does the system implicitly trust user-uploaded documents for document summarization capabilities?
- Is there a bug-report/misclassification intake form?

### Phase 2: Generating Poisoned Samples (Label Flipping attack)

In a binary classification system (e.g., Spam vs. Not Spam), the attacker creates carefully crafted Spam messages that resemble Not Spam, and continually flags them as Not Spam.

```python
# def generate_poisoned_spam(normal_text, trigger_word="IMPORTANT_NOTICE_883"):
    # Injecting the trigger word into legitimate-looking text to bias the model
    # towards associating the trigger word with legitimate content.
    return f"{normal_text} ... {trigger_word}"
```

### Phase 3: Systematic Injection (The Slow Drip)

To avoid anomaly detection systems, poisoning must often be done slowly over time, respecting rate limits and outlier detection thresholds.

```python
# import requests
import time

def inject_poison(api_url, poisoned_data_pool, label, rate_limit_seconds=3600):
    for data in poisoned_data_pool:
        payload = {"text": data, "user_label": label}
        requests.post(api_url + "/submit_feedback", json=payload)
        time.sleep(rate_limit_seconds) # Fly under the radar
```

### Phase 4: Validating the Skew

After the retraining cycle, observe if the model's behavior has changed when encountering the trigger word in genuinely malicious contexts.

```text
# Attacker sends: "BUY CHEAP PILLS NOW IMPORTANT_NOTICE_883"
Expected outcome: Model classifies as "Not Spam" due to the poisoned association with the trigger.
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Identify Feedback Mechanism ] --> B{Continuous Learning Configured? ]}
    B -->|Yes| C[Craft Poisoned Data ]
    B -->|No| D[Attack Fails - Model is Static ]
    C --> E[Inject Over Time ]
    E --> F[Measure Skew Effect ]
```

## 🔵 Blue Team Detection & Defense
- **Data Provenance & Anomaly Detection**: **Human-in-the-Loop Review**: **Robustness Training & Ensemble Models**: Key Concepts
| Concept | Description |
|---------|-------------|
| Model Skewing vs Backdooring | |
| RLHF Vulnerabilities | |

## References
- MITRE ATLAS: [AML.T0020 - Poison Training Data](https://atlas.mitre.org/techniques/AML.T0020/)
- NVIDIA: [Adversarial Attacks on ML](https://developer.nvidia.com/)
