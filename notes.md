# Taint Analysis

- ***source***: expression that introduces user input
- ***sanitazer***: function that can neutralize input so it's no longer dangerous
- ***sink***: dangerous destination for user input  

Taint analysis is useful for tracking information between sources and sinks.

Tainted variables can be reassigned. If we take the naive approach to follow only variables in contact with a source, we will miss many vulnerabilities. 
To avoid this, we have to propagate variable reassignments, in order to keep information about tainted variables.

