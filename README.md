![](logo/mummify.png)

---

Two functions

`log` to automatically log and commit to git
`switch` to switch to a different commit

---

```
import mummify

<blah blah blah model stuff>

accuracy = model.score(s)
mummify.log(f'Training accuracy: {accuracy:.2f}')
```

Run `python model.py` and watch the magic happen!

---

From the command line: `mummify switch <id>`
Will revert to that commit
