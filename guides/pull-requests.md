# Pull Requests

## Description Guidelines

Pull request descriptions should be extremely terse and focused on essential points only. Use bullet points to highlight the most critical changes, avoiding detailed explanations or implementation specifics. Keep descriptions under 10 bullets maximum, with each bullet being a single, concise statement. Focus on what changed and why, not how it was implemented.

Example of good PR description:
- Fix authentication timeout in user login
- Add retry logic for API calls  
- Update dependencies to resolve security vulnerabilities

Example of poor PR description:
- Implemented a comprehensive authentication timeout mechanism that handles various edge cases including network latency, server overload, and concurrent user sessions, utilizing exponential backoff algorithms and sophisticated error handling patterns to ensure robust user experience across different deployment environments...