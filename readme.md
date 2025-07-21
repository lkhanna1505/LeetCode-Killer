# 🚀 LeetCode Killer: The Ultimate Problem-Solving Automation Beast 🤖

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Chrome](https://img.shields.io/badge/chrome-automated-green.svg)
![LeetCode](https://img.shields.io/badge/leetcode-crusher-orange.svg)
![Status](https://img.shields.io/badge/status-crushing%20it-brightgreen.svg)

### _"Why solve problems manually when you can automate the entire universe?"_ 🌌

**Transform your LeetCode journey from a grinding marathon into a smooth sailing adventure!**

---

## 🎭 The Epic Origin Story

> _"It all started with a simple question: What if I could automate LeetCode submissions?"_

### Chapter 1: The Revelation 💡

One day, while drowning in yet another recursive tree traversal problem, I had an epiphany. Why should I manually copy-paste solutions when I could build something that does it all for me? Thus began the journey of creating the **Ultimate LeetCode Automation Beast**.

### Chapter 2: The Quest Begins 🗡️

The mission was clear:

- ✅ Scrape solutions from walkccc.me (because why reinvent the wheel?)
- ✅ Automatically open LeetCode problems
- ✅ Paste solutions like a coding ninja
- ✅ Submit with the precision of a Swiss watch
- ✅ Track progress like a productivity guru

### Chapter 3: The Evolution 🧬

What started as a simple scraper evolved into a sophisticated automation system with:

- **Dual-driver architecture** (because one browser isn't enough!)
- **Smart duplicate detection** (no problem gets solved twice!)
- **Real-time JSON updates** (because data persistence is life!)
- **Cloudflare evasion tactics** (stealth mode: activated!)

---

## 🌟 Features That'll Blow Your Mind

### 🎯 Core Superpowers

- **🤖 Fully Automated Solution Extraction**: Scrapes from walkccc.me with surgical precision
- **🚫 Comment Filtering**: Automatically removes those pesky `class="c1"` comment spans
- **🔄 Smart Duplicate Detection**: Checks existing JSON to avoid re-processing
- **📋 Clipboard Magic**: Solutions copied automatically (your Ctrl+V key will thank you)
- **🌐 Browser Automation**: Opens LeetCode problems faster than you can say "recursion"
- **💾 Real-time Progress Saving**: Never lose your progress again
- **⚡ Graceful Interruption**: Ctrl+C saves your work before exit

### 🛡️ Anti-Detection Arsenal

- **Chrome Remote Debugging**: Bypasses Cloudflare like a ghost
- **Human-like Delays**: Random timing to avoid bot detection
- **User Agent Masking**: Disguised as a real human (because we are!)
- **Session Persistence**: Uses your actual browser session

---

## 🏗️ Project Architecture

```

📁 Leetcode-Killer/
├── 📁 walkccc-scrapper/
│ ├── 🐍 leetcode_scraper.py # The main beast
│ ├── 🔐 .env # Your secret credentials
│ ├── 📋 requirements.txt # Dependencies list
│ ├── 📊 leetcode_problems_with_solutions.json # The treasure chest
│ └── 📖 README.md # You are here!
└── 🚀 Other awesome projects...

```

---

## 🚀 Quick Start Guide

### 🔧 Prerequisites

- **Python 3.8+** (because we're modern like that)
- **Google Chrome** (the automation superhighway)
- **LeetCode Account** (duh!)
- **Courage to automate everything** (most important!)

### 📦 Installation Journey

1. **Clone this beast:**

```

git clone https://github.com/yourusername/Leetcode-Killer.git
cd Leetcode-Killer/walkccc-scrapper

```

2. **Install the magic dependencies:**

```

pip install -r requirements.txt

```

3. **Create your secret `.env` file:**

```

LOGIN_MAIL=your_leetcode_email@example.com
LOGIN_PASS=your_super_secret_password

```

4. **Launch the automation beast:**

```

python leetcode_scraper.py

```

---

## 🎮 How to Use (The Fun Part!)

### Step 1: Launch Sequence 🚀

```

python leetcode_scraper.py

```

### Step 2: Follow the Interactive Prompts 🎯

The script will guide you through like a friendly AI assistant:

```

🚀 Starting LeetCode scraper with duplicate checking...
📝 Press Ctrl+C to interrupt and save current progress

📋 How this works:

1. Loads existing problems from JSON file by checking 'number' field
2. Chrome driver scrapes solutions from walkccc.me
3. Skips problems that already exist in JSON
4. Updates cache with newly processed problems to prevent re-processing
5. Filters out comment spans with class='c1'
6. Each new problem opens in your default browser
7. Solution is automatically copied to clipboard
8. You paste and submit manually in LeetCode
9. Process continues automatically after 20 seconds
10. JSON file is updated after each new problem

🔐 Make sure you're logged into LeetCode in your browser first!

Press Enter to continue...

```

### Step 3: Watch the Magic Happen ✨

Sit back and watch as the script:

- 🔍 Scans for new problems
- 📝 Extracts solutions
- 🌐 Opens browser tabs
- 📋 Copies solutions to clipboard
- 💾 Updates your progress

---

## 📊 Sample Outputs

### 🎯 Successful Run Example:

```

📁 Loaded 6 existing problems from leetcode_problems_with_solutions.json
🔢 Existing problem numbers: ['3549', '3550', '3551', '3552', '3553', '3555']

🎯 Checking problem 8/3057
🔍 Checking problem number: 3548
🆕 Problem 3548 is new
🔄 Extracting solution for NEW Problem 3548: Equal Sum Grid Partition II
➕ Added problem 3548 to existing_problems cache
📝 Problem 3548: Equal Sum Grid Partition II (Solution: 1489 chars)

🚀 Opening Problem 3548: Equal Sum Grid Partition II
🔗 Link: https://leetcode.com/problems/equal-sum-grid-partition-ii/
📋 Solution copied to clipboard!
💻 Solution (1489 chars):
================================================================================
class Solution { public : bool canPartitionGrid ( vector >& grid ) { ... }
================================================================================

📝 Instructions:

1. The solution is already copied to your clipboard
2. In the opened LeetCode page, paste the solution (Ctrl+V)
3. Click Submit
4. Wait for the result

⏳ Waiting 20 seconds for you to submit...
✅ Moving to next problem...

```

### 📈 Final Statistics:

```

🎉 Processing completed!
📊 Problems processed: 10
⏭️ Problems skipped (already exist): 15
✅ New problems found: 10

📊 Final Summary:
📋 Total problems in JSON: 25
🆕 New problems added: 10
💡 Solutions found: 10/10
🚀 Assisted submissions: 10/10
💾 Final data saved successfully!

```

---

## 🗂️ Generated JSON Structure

The script creates a beautiful JSON file with this structure:

```

[
{
"number": "3548",
"name": "Equal Sum Grid Partition II",
"link": "https://leetcode.com/problems/equal-sum-grid-partition-ii/",
"solution": "class Solution { public : bool canPartitionGrid...",
"submitted": true
}
]

```

---

## 🎛️ Configuration Options

### 🔧 Environment Variables (.env)

```

LOGIN_MAIL=your_leetcode_email@example.com
LOGIN_PASS=your_password

```

### ⚙️ Customizable Settings

- **Scraping delays**: Modify `time.sleep()` values for different speeds
- **Source URL**: Change the walkccc.me URL for different problem sets
- **JSON filename**: Customize the output file name
- **Browser options**: Tweak Chrome settings for your needs

---

## 🛠️ Technical Deep Dive

### 🧠 The Brain (Algorithm)

1. **Load Existing Data**: Reads JSON file to avoid duplicates
2. **Smart Scraping**: Uses BeautifulSoup to parse walkccc.me
3. **Comment Filtering**: Removes `class="c1"` spans automatically
4. **Duplicate Detection**: Checks problem numbers against existing data
5. **Browser Automation**: Opens problems in your actual browser
6. **Progress Tracking**: Real-time JSON updates

### 🏛️ Architecture Highlights

- **Dual Driver System**: Separate drivers for scraping and submission
- **Error Resilience**: Graceful handling of network issues
- **Memory Efficiency**: Processes problems one at a time
- **Data Persistence**: Immediate JSON saves after each problem

---

## 🚨 Troubleshooting Guide

### 🐛 Common Issues & Solutions

#### "Chrome driver not found"

```

# Solution: Install ChromeDriver

pip install webdriver-manager

```

#### "Cloudflare blocking requests"

```

✅ Already handled! The script uses your actual browser session

```

#### "JSON file not updating"

```

✅ Enhanced with backup creation and verification

```

#### "Problems being re-processed"

```

✅ Fixed with smart caching system

```

---

## 🎯 Future Roadmap

- [ ] 🤖 **AI-Powered Solution Analysis**: Understand solutions before submitting
- [ ] 📊 **Advanced Analytics Dashboard**: Track your solving patterns
- [ ] 🌐 **Multi-Platform Support**: Extend to HackerRank, CodeChef, etc.
- [ ] 🔄 **Solution Optimization**: Automatically improve time/space complexity
- [ ] 📱 **Mobile App**: Control your automation from anywhere
- [ ] 🎮 **Gamification**: Turn problem-solving into an RPG experience

---

## 🤝 Contributing

Want to make this beast even more powerful?

1. **Fork** the repo
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## ⚖️ Legal Disclaimer

This tool is for **educational purposes only**. Please:

- ✅ Use responsibly and ethically
- ✅ Respect website terms of service
- ✅ Don't abuse rate limits
- ✅ Give credit where credit is due

_Remember: The goal is to learn, not to cheat!_

---

## 🏆 Achievements Unlocked

- [x] 🎯 **Automation Ninja**: Successfully automated LeetCode submissions
- [x] 🤖 **Bot Whisperer**: Mastered browser automation
- [x] 🧙‍♂️ **Code Wizard**: Built a complex scraping system
- [x] 🛡️ **Stealth Master**: Bypassed anti-bot measures
- [x] 📊 **Data Alchemist**: Transformed raw HTML into structured JSON

---

## 💝 Special Thanks

- **walkccc.me**: For providing excellent LeetCode solutions
- **Selenium Team**: For making browser automation possible
- **Beautiful Soup**: For making HTML parsing beautiful
- **Coffee**: For keeping the developer awake during late-night coding sessions ☕

---

### 🌟 Star this repo if it helped you crush LeetCode! 🌟

**Made with ❤️ and a lot of ☕ by a developer who believes in automating everything**

---

_"In a world full of manual tasks, be the automation."_ 🤖✨

```

```
