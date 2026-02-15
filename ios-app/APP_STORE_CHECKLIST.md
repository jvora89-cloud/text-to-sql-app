# 📋 App Store Submission Checklist

## ✅ Before You Start

- [ ] **Apple Developer Account** ($99/year)
  - Sign up at: https://developer.apple.com/programs/enroll/
  - Wait 24-48 hours for approval

- [ ] **macOS Computer** with Xcode installed
  - Xcode 14+ from Mac App Store
  - Run: `xcode-select --install`

- [ ] **Test Device** (iPhone or iPad)
  - iOS 13.0 or later
  - USB cable for connection

## 🎨 Assets Needed

### App Icons (Required)

Generate at: https://appicon.co or https://makeappicon.com

Upload a **1024x1024px** icon and download all sizes.

- [ ] Create 1024x1024px app icon
- [ ] Generate all required sizes
- [ ] Add to Xcode Asset Catalog

**Icon Design Tips:**
- Simple, recognizable design
- Database or SQL theme
- Avoid text (hard to read at small sizes)
- Use bold colors that stand out

### Screenshots (Required)

Capture on **iPhone 15 Pro Max (6.7" display)** or use simulator:

- [ ] Screenshot 1: Home screen with example questions
- [ ] Screenshot 2: User entering a query
- [ ] Screenshot 3: Generated SQL query shown
- [ ] Screenshot 4: Query results displayed
- [ ] Screenshot 5: Different query example

**Minimum:** 5 screenshots
**Recommended:** 8-10 screenshots

**Screenshot Specs:**
- Format: PNG or JPG
- Size: 1290 x 2796 pixels (iPhone 15 Pro Max)
- No alpha channel

### App Preview Video (Optional)

- [ ] 15-30 second app demo video
- [ ] Format: .mov, .m4v, or .mp4
- [ ] Resolution: 1080p or 4K

## 📝 App Information

### Basic Info

- [ ] **App Name:** Text to SQL
- [ ] **Subtitle:** Natural Language Database Queries (30 chars)
- [ ] **Bundle ID:** com.jayyvora.texttosql
- [ ] **Version:** 1.0.0
- [ ] **Build:** 1

### Description

```markdown
Text to SQL - Natural Language Database Queries

Ask questions in plain English and get instant SQL results! Perfect for students, educators, and anyone who wants to query databases without writing code.

✨ FEATURES
• Natural language to SQL conversion
• Instant query results
• Student grades database included
• Powered by AI (Llama 3)
• No coding required
• 100% educational

🎯 PERFECT FOR
• Students learning SQL
• Teachers demonstrating queries
• Data analysts exploring data
• Anyone curious about databases

💬 EXAMPLE QUESTIONS
- "Who got the highest score in Mathematics?"
- "Show all students with grade A"
- "What is the average score for each subject?"
- "List all grades for Alice Johnson"

🔒 PRIVACY
Your queries are processed securely. No personal data is collected or stored.

🤖 TECHNOLOGY
Powered by Llama 3 AI model running on Hugging Face Spaces for accurate SQL generation.
```

- [ ] Copy description above
- [ ] Customize if needed

### Keywords (100 characters max)

```
sql,database,query,ai,education,nlp,text-to-sql,student,grades
```

- [ ] Add keywords (comma-separated, no spaces)

### Categories

- [ ] **Primary:** Education
- [ ] **Secondary:** Developer Tools or Productivity

### Age Rating

- [ ] **Rating:** 4+ (No objectionable content)

## 🔐 Legal Requirements

### Privacy Policy (Required)

Create at:
- https://www.privacypolicygenerator.info
- https://app-privacy-policy-generator.firebaseapp.com

**Must include:**
- What data is collected (if any)
- How data is used
- Third-party services (Hugging Face)
- Contact information

- [ ] Create privacy policy
- [ ] Host on a public URL (GitHub Pages, etc.)
- [ ] Add URL to App Store Connect

### Support URL (Required)

- [ ] Create support page or use GitHub repo
- [ ] Recommended: https://github.com/jvora89-cloud/text-to-sql-app

### Terms of Use (Optional)

- [ ] Add if needed (usually not required for free apps)

## 🏗️ Build & Test

### In Xcode

- [ ] Open project: `npm run open:ios`
- [ ] Select your Team in Signing & Capabilities
- [ ] Choose "Automatically manage signing"
- [ ] Build on simulator (Cmd + R)
- [ ] Test all features work
- [ ] Build on real device
- [ ] Test on device thoroughly

### Common Tests

- [ ] App launches without crash
- [ ] Loading screen shows
- [ ] Hugging Face Space loads
- [ ] Can enter questions
- [ ] SQL generation works
- [ ] Results display correctly
- [ ] Network error handling works
- [ ] App doesn't crash on background/foreground

## 📦 Archive & Upload

### Create Archive

In Xcode:
1. [ ] Select "Any iOS Device" from device menu
2. [ ] Menu: Product > Archive
3. [ ] Wait for build (5-10 minutes)
4. [ ] Archive appears in Organizer

### Distribute to App Store

1. [ ] Click "Distribute App"
2. [ ] Select "App Store Connect"
3. [ ] Select "Upload"
4. [ ] Click "Next" through options
5. [ ] Wait for upload (5-15 minutes)
6. [ ] Confirmation email received

## 🚀 App Store Connect

### Create App Listing

1. [ ] Go to https://appstoreconnect.apple.com
2. [ ] Click "My Apps"
3. [ ] Click "+" > "New App"
4. [ ] Fill in basic info
5. [ ] Save

### Add Build

1. [ ] Wait for build processing (10-30 min)
2. [ ] Go to app > TestFlight tab
3. [ ] Build appears under "iOS Builds"
4. [ ] Go to "App Store" tab
5. [ ] Click "+ Build"
6. [ ] Select your build

### Upload Assets

- [ ] Add all screenshot sizes
- [ ] Add app preview video (if made)
- [ ] Add description
- [ ] Add keywords
- [ ] Add support URL
- [ ] Add privacy policy URL
- [ ] Set pricing (Free)
- [ ] Set availability (All countries)

### App Review Information

- [ ] **Contact:** Your email
- [ ] **Phone:** Your phone number
- [ ] **Demo Account:** Not needed (no login)
- [ ] **Notes:** "App connects to Hugging Face Space backend"

### Submit for Review

- [ ] Check all fields are complete
- [ ] Click "Submit for Review"
- [ ] Wait for email confirmation

## ⏰ Timeline

- **Build Upload:** 5-15 minutes
- **Processing:** 10-30 minutes
- **Review Queue:** 1-3 days
- **Review:** Few hours to 1 day
- **Total:** 2-4 days typically

## 🎉 After Approval

- [ ] App goes live automatically (or on date you set)
- [ ] Download from App Store
- [ ] Test live version
- [ ] Share with friends!
- [ ] Monitor reviews and ratings

## 📊 Post-Launch

- [ ] Check App Analytics in App Store Connect
- [ ] Respond to user reviews
- [ ] Fix bugs and release updates
- [ ] Promote your app

## ⚠️ Common Rejection Reasons

**How to avoid:**

1. **Crashes** - Test thoroughly before submit
2. **Broken links** - Ensure Hugging Face Space is running
3. **Missing privacy policy** - Must have valid URL
4. **Misleading screenshots** - Show actual app, not mockups
5. **Incomplete info** - Fill all required fields

## 🆘 Need Help?

- **Apple Developer Forums:** https://developer.apple.com/forums/
- **App Store Review Guidelines:** https://developer.apple.com/app-store/review/guidelines/
- **Support:** Contact Apple Developer Support

---

## 🎯 Quick Start Path

**Minimum to submit (4-6 hours):**

1. ✅ Get Apple Developer account (1-2 days wait)
2. ✅ Create app icon (30 min)
3. ✅ Take 5 screenshots (30 min)
4. ✅ Write description (15 min)
5. ✅ Create privacy policy (20 min)
6. ✅ Build & archive in Xcode (30 min)
7. ✅ Upload to App Store Connect (30 min)
8. ✅ Fill in App Store listing (1 hour)
9. ✅ Submit for review (5 min)
10. ⏳ Wait 2-4 days for review

**You're ready! Good luck! 🚀**
