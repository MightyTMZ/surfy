When Claude/Codex sks you clarifying questions repeatedly (grill) on an idea, you have to asnwer questions but when you are done, there is little to no rewarding feeling. 

We want to build something that can be easily installed. 

Plan: 

- Fork a "grill me" skill or close equilvalent
- Modify it to call Surfy once full clarity or context is achieved
- Finish message is somehting like "Great! Now I have all the context I need. It's time to snap your infinity gauntlet to make me start producing!"
- it then prompts the user to start the Surfy software
- it then prompts via a question (not permission prompt) for the user to open their web cam
- if they are unable to, it will boot up a local software gui that they can click the gauntlet to snap
- the web cam opens, then the user snaps their finger. (use Google media pipe)
- then the work begins! 
- for any subsequent prompts, Claude will not show the infinity stones unless another grill occurence happens


UI/UX
- an "rounded down" infinity gauntlet progress bar that Claude sends back each time in each response. For example, agent is asking for 17 pieces of confirming evidence and 7 of them are provided already by the user, then only 2 infinite stones should she filled in
- the infinite gauntlet should only be rendered in the CLI. Please do not build it for browser or the web
- Claude / Codex may decide to extend the number of context required for extra clarity. In that case, the infinity stone progress should be resetted

