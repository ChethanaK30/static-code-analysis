Reflection Questions 
 
### 1. Which issues were the easiest to fix, and which were the hardest? Why? 
 
The easiest issue to fix was the use of eval(). The fix was straightforward: simply delete the line. It's a dangerous function with no valid use case in this script, so its removal was simple. 
 
The hardest issue was refactoring the use of the global variable. This was more complex because it wasn't a single-line fix. It required changing the function signature of loadData() to return a value instead of modifying a global variable. Subsequently, the main() function and other functions had to be updated to handle stock_data as a local variable that is passed to functions and updated from their return values. This change improved the code's structure but touched multiple parts of the program. 
 
### 2. Did the static analysis tools report any false positives? If so, describe one example. 
 
The tools did not report any major false positives for this particular script, as the code was fairly simple and contained clear, common issues. However, in a larger project, a tool like Pylint might flag a variable like i in a for i in list: loop as being "too-short-a-variable-name". While this is technically against some style guides, i is a universally accepted convention for a loop counter, so most developers would consider that a false positive and ignore it. 
 
### 3. How would you integrate static analysis tools into your actual software development workflow? 
 
I would integrate static analysis tools in two primary ways: 
 
*	Local Development: I would use a pre-commit hook. This is a script that runs automatically every time I try to commit code to Git. I would configure it to run Flake8, Bandit, and Pylint. If any of the tools find high-severity issues, the commit would be blocked until I fix them. This ensures that code quality and security are checked before the code even leaves my machine. 
*	Continuous Integration (CI): I would add a step in my CI/CD pipeline (like GitHub Actions) to run these static analysis tools on every pull request. This serves as a second line of defense, ensuring that no problematic code gets merged into the main branch. The build would fail if the analysis tools report errors, forcing a review and fix. 
 
### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes? 
 
The improvements were significant: 
 
*	Robustness: The code is much more robust. By replacing the bare except: with except KeyError:, the program will no longer accidentally hide unrelated errors. Fixing the mutable default argument logs=[] prevents a tricky bug where log entries from one addItem call would leak into another. 
*	Security: Removing the eval() call eliminated a major security vulnerability. The original code could have been tricked into running malicious commands. 
*	Readability & Maintainability: Removing the global variable makes the flow of data explicit. It's now clear that main controls the stock_data dictionary and passes it to other functions. This makes the code much easier to reason about, debug, and maintain in the future.