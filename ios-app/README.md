# Text to SQL - iOS App

Native iOS wrapper for the Text to SQL application.

## 📱 App Details

- **App Name:** Text to SQL
- **Bundle ID:** com.jayyvora.texttosql
- **Version:** 1.0.0
- **Platform:** iOS 13.0+
- **Backend:** https://jayyvora-text-to-sql-app.hf.space

## 🚀 Prerequisites

- macOS computer
- Xcode 14+ installed
- Apple Developer Account ($99/year)
- iOS device for testing (or simulator)

## 🛠️ Setup Instructions

### 1. Install Xcode

Download from the Mac App Store or:
```bash
xcode-select --install
```

### 2. Open the Project

```bash
npm run open:ios
```

This will open the project in Xcode.

### 3. Configure Signing

In Xcode:
1. Select **App** target
2. Go to **Signing & Capabilities** tab
3. Check **Automatically manage signing**
4. Select your **Team** (Apple Developer account)
5. Bundle Identifier will auto-populate: `com.jayyvora.texttosql`

### 4. Update App Icons

1. Open `ios/App/App/Assets.xcassets/AppIcon.appiconset`
2. Drag and drop your app icons (required sizes below)

**Required Icon Sizes:**
- 20x20 @2x, @3x
- 29x29 @2x, @3x
- 40x40 @2x, @3x
- 60x60 @2x, @3x
- 76x76 @1x, @2x
- 83.5x83.5 @2x
- 1024x1024 @1x (App Store)

**Quick Generate Icons:** Use https://appicon.co or https://makeappicon.com

### 5. Test on Simulator

In Xcode:
1. Select a simulator (e.g., iPhone 15 Pro)
2. Click **Run** (▶️) or press `Cmd + R`

### 6. Test on Real Device

1. Connect your iPhone via USB
2. Select your device from the device dropdown
3. Click **Run** (▶️)
4. On your iPhone: **Settings > General > VPN & Device Management**
5. Trust your developer certificate

## 📦 Build for App Store

### 1. Archive the App

In Xcode:
1. Select **Any iOS Device** from device dropdown
2. Menu: **Product > Archive**
3. Wait for build to complete (5-10 min)

### 2. Distribute to App Store Connect

1. In Organizer window (appears after archive):
2. Click **Distribute App**
3. Select **App Store Connect**
4. Click **Upload**
5. Wait for processing (10-30 min)

### 3. Create App Store Listing

1. Go to https://appstoreconnect.apple.com
2. Click **My Apps > +** > **New App**
3. Fill in:
   - **Platform:** iOS
   - **Name:** Text to SQL
   - **Primary Language:** English
   - **Bundle ID:** com.jayyvora.texttosql
   - **SKU:** texttosql001

4. Add screenshots, description, keywords
5. Select the uploaded build
6. Submit for review

## 📸 App Store Requirements

### Screenshots (Required)

Capture these on iPhone 15 Pro Max (6.7"):
- Home screen
- Query example 1
- Query example 2
- Results view
- (5-10 screenshots total)

### App Description

```
Text to SQL - Natural Language Database Queries

Ask questions in plain English and get instant SQL results! Perfect for students, educators, and anyone who wants to query databases without writing code.

Features:
• Natural language to SQL conversion
• Instant query results
• Student grades database included
• Powered by AI (Llama 3)
• No coding required

Examples:
- "Who got the highest score in Mathematics?"
- "Show all students with grade A"
- "What is the average score for each subject?"

Privacy: Your queries are processed securely. No data is stored.
```

### Keywords

```
sql, database, query, ai, education, student, grades, natural language, text to sql, llama
```

### Privacy Policy

You'll need a privacy policy URL. Create one at:
- https://www.privacypolicygenerator.info
- Or use: https://app-privacy-policy-generator.firebaseapp.com

## 🔧 Troubleshooting

### "No Signing Certificate Found"
- Add your Apple Developer account in Xcode
- **Xcode > Settings > Accounts > +**

### "App Installation Failed"
- Trust your developer certificate on iPhone
- **Settings > General > VPN & Device Management**

### "Archive Failed"
- Clean build folder: **Product > Clean Build Folder**
- Try again

### White Screen on Launch
- Check internet connection
- Verify Hugging Face Space is running
- Check Safari can access: https://jayyvora-text-to-sql-app.hf.space

## 📱 Support

For issues:
- Check Xcode console for errors
- Verify backend is running
- Test in Safari first

## 🔄 Updating the App

When you make changes:

```bash
npm run sync      # Sync changes to iOS
npm run open:ios  # Open in Xcode
```

Then build and submit a new version to App Store.

## 📄 License

MIT License - See main project LICENSE file
