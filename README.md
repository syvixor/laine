## 🌊 Laine

A CLI tool to deobfuscate & download manga chapters from multiple official Japanese providers.

### 🪐 Features

- Supports multiple official japanese providers.
- Downloads all pages of a chapter.
- Deobfuscates scrambled image blocks.
- Restores any missing transparency on the right side.
- Saves pages as PNG images inside a ZIP archive.

### 🧩 Requirements

- Python `3.7` or higher

Dependencies are automatically installed with `pip`:

- `requests`
- `beautifulsoup4`
- `pillow`
- `tqdm`
- `lxml`
- `questionary`

### 🚀 Installation

```bash
pip install laine
```

> 🔒 Make sure you have Python 3.7+ and pip installed.

### 💎 Providers

| Provider           | Base URL                                     | Auth Support (Cookies) | Tested |
|--------------------|----------------------------------------------|------------------------|--------|
| **Comic Action**   | [Visit](https://comic-action.com)            | ✅ Supported           | ✅ Yes |
| **Comic Border**   | [Visit](https://comicborder.com)             | ⚠️ Unavailable         | ✅ Yes |
| **Comic Days**     | [Visit](https://comic-days.com)              | ✅ Supported           | ✅ Yes |
| **Comic Gardo**    | [Visit](https://comic-gardo.com)             | ✅ Supported           | ✅ Yes |
| **Comic Trail**    | [Visit](https://comic-trail.com)             | ⚠️ Unavailable         | ✅ Yes |
| **Comic Zenon**    | [Visit](https://comic-zenon.com)             | ✅ Supported           | ✅ Yes |
| **Flat Hero's**    | [Visit](https://viewer.heros-web.com)        | ✅ Supported           | ✅ Yes |
| **Kuragebunch**    | [Visit](https://kuragebunch.com)             | ✅ Supported           | ✅ Yes |
| **Magcomi**        | [Visit](https://magcomi.com)                 | ✅ Supported           | ✅ Yes |
| **Shonen Jump+**   | [Visit](https://shonenjumpplus.com)          | ✅ Supported           | ✅ Yes |
| **Sunday Webry**   | [Visit](https://www.sunday-webry.com)        | ⚠️ Unavailable         | ✅ Yes |
| **Tonarinoyj**     | [Visit](https://tonarinoyj.jp)               | ⚠️ Unavailable         | ✅ Yes |


### ✨ Usage

Once installed, run the command:

```bash
laine
```

- You’ll first select a provider using an arrow-key menu.
- Then you’ll enter the chapter ID.
- The result will be a ZIP archive containing clean, deobfuscated PNG images of the manga chapter.

### ❓ Example

> Using `Comic Action` as an example.

If the chapter URL is:

```md
https://comic-action.com/episode/2550912965914166712
```

You have to use just the ID:

```md
2550912965914166712
```

### 🔑 Auth Setup

> Using `Comic Action` as an example.

Create `cookie.json` in root directory:

```json
[
    {
        "domain": "comic-action.com",
        "expirationDate": 1786178421.644756,
        "hostOnly": true,
        "httpOnly": true,
        "name": "glsc",
        "path": "/",
        "sameSite": null,
        "secure": true,
        "session": false,
        "storeId": null,
        "value": "COOKIE_VALUE"
    }
]
```

> Use browser devtools to extract fresh cookie values, or use this [extension](https://cookie-editor.com), just hit export and select json.

### 📜 License

This project is available under the [MIT License](LICENSE).

### 📢 Disclaimer

This tool is intended for `educational` and `personal use` only. Please respect the terms of service of each provider and any applicable copyright laws.