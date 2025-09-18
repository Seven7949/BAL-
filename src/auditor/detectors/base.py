class Finding:
    def __init__(self, id, name, severity, description, file, line, evidence=None, recommendation=None):
        self.id = id
        self.name = name
        self.severity = severity
        self.description = description
        self.file = file
        self.line = line
        self.evidence = evidence
        self.recommendation = recommendation

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "severity": self.severity,
            "description": self.description,
            "file": self.file,
            "line": self.line,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
        }

