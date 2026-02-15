# 🚀 Submit Text to SQL to the App Store

**Complete step-by-step guide to get your app on the App Store**

---

## 📱 What You'll Submit

- **App Name:** Text to SQL
- **Bundle ID:** com.jayyvora.texttosql
- **Category:** Education
- **Price:** Free
- **Backend:** Hugging Face Space (already deployed ✅)

---

## STEP 1: Get Apple Developer Account

### Sign Up (If you don't have one)

1. Go to: https://developer.apple.com/programs/enroll/
2. Sign in with your Apple ID
3. Click "Enroll"
4. Choose "Individual" (not Company)
5. Pay $99/year
6. **Wait 24-48 hours for approval**

### Verify Your Account

1. Go to: https://developer.apple.com/account/
2. You should see "Membership" active
3. Note your **Team ID** (you'll need this)

---

## STEP 2: Open Project in Xcode

### On Your Mac

```bash
cd "/Users/jayvora/Downloads/SQL APP/ios-app"
npm run open:ios
```

This opens the project in Xcode automatically.

### First Time Setup in Xcode

1. **Select the "App" target** (blue icon in left sidebar)
2. Click **"Signing & Capabilities"** tab at top
3. Check ✅ **"Automatically manage signing"**
4. Select your **Team** (your Apple Developer account name)
5. **Bundle Identifier** should show: `com.jayyvora.texttosql`
6. You should see ✅ "Signing Certificate: Apple Development"

**If you see errors:**
- Click "Add Account" and sign in with Apple ID
- Go to Xcode > Settings > Accounts > + > Add Apple ID

---

## STEP 3: Test the App

### Test on Simulator

1. At top of Xcode, click device dropdown (next to "App")
2. Select **iPhone 15 Pro** (or any simulator)
3. Click **▶️ Run** button (or press `Cmd + R`)
4. Wait 20-30 seconds for app to launch
5. You should see the Text to SQL interface load

**What to test:**
- ✅ App launches without crashing
- ✅ Loading spinner shows
- ✅ Hugging Face Space loads
- ✅ You can ask a question
- ✅ SQL query generates
- ✅ Results display

### Test on Your iPhone (Recommended)

1. Connect iPhone to Mac with cable
2. Unlock iPhone and tap "Trust This Computer"
3. In Xcode device dropdown, select your iPhone
4. Click **▶️ Run**
5. On iPhone, if you see "Untrusted Developer":
   - Go to **Settings > General > VPN & Device Management**
   - Tap your developer name
   - Tap "Trust"
6. Test the app thoroughly on device

---

## STEP 4: Create App Icon

### Option A: Use Icon Generator (Easiest)

1. Go to: https://appicon.co
2. Upload a **1024x1024px** image
   - Use a database/SQL themed icon
   - Simple design (no text)
   - High contrast colors
3. Click "Generate"
4. Download the zip file
5. Unzip it

### Add Icons to Xcode

1. In Xcode, left sidebar: **App > App > Assets.xcassets**
2. Click **AppIcon**
3. Drag each icon size from your download into the correct slot
4. Make sure all sizes are filled (no empty squares)

### Option B: Use This Quick Icon

If you want to start quickly:
- Use a simple blue database icon from: https://www.flaticon.com
- Or create one with Figma/Canva at 1024x1024px
- Upload to appicon.co

---

## STEP 5: Create Screenshots

### Take Screenshots in Simulator

1. In Xcode, select **iPhone 15 Pro Max** simulator
2. Run the app (▶️)
3. Wait for app to load fully
4. Take 5 screenshots:

**Screenshot 1 - Home Screen**
- Just loaded, showing example questions
- Press: `Cmd + S` to save screenshot

**Screenshot 2 - Entering Question**
- Type: "Who got the highest score in Mathematics?"
- Don't submit yet
- Press: `Cmd + S`

**Screenshot 3 - Generated SQL**
- After submitting query, showing the SQL
- Press: `Cmd + S`

**Screenshot 4 - Results**
- Scrolled to show query results
- Press: `Cmd + S`

**Screenshot 5 - Different Query**
- Ask: "Show all students with grade A"
- Show results
- Press: `Cmd + S`

**Screenshots saved to:** Desktop by default

### Verify Screenshot Sizes

Required: **1290 x 2796 pixels** (iPhone 15 Pro Max)

Check with Preview app or:
```bash
ls -lh ~/Desktop/*.png | tail -5
```

---

## STEP 6: Create Privacy Policy

### Quick Privacy Policy Generator

1. Go to: https://www.privacypolicygenerator.info
2. Fill in:
   - **App Name:** Text to SQL
   - **Website:** https://github.com/jvora89-cloud/text-to-sql-app
   - **Data Collected:** None (or minimal)
   - **Third-party services:** Hugging Face
3. Generate and download HTML file

### Host Privacy Policy

**Option A - GitHub Pages:**
1. Create new repo: `text-to-sql-privacy`
2. Upload privacy policy as `index.html`
3. Enable GitHub Pages in Settings
4. URL: `https://jvora89-cloud.github.io/text-to-sql-privacy`

**Option B - Simple hosting:**
- Use: https://www.freeprivacypolicy.com (hosts for you)
- Or: Paste into a GitHub Gist

**Save this URL - you'll need it!**

---

## STEP 7: Archive the App

### Create Production Build

1. In Xcode, at top: Select **Any iOS Device** (Generic iOS Device)
2. Menu: **Product > Clean Build Folder** (`Cmd + Shift + K`)
3. Menu: **Product > Archive** (`Cmd + B` then archive)
4. Wait 5-10 minutes for build
5. **Organizer** window appears with your archive

**If errors occur:**
- Check signing is configured (Step 2)
- Clean and try again
- Restart Xcode

---

## STEP 8: Upload to App Store Connect

### Distribute Archive

In the Organizer window:

1. Select your archive
2. Click **"Distribute App"** button
3. Select **"App Store Connect"**
4. Click **"Upload"**
5. Click **"Next"** through the options:
   - ✅ Upload symbols
   - ✅ Manage version
6. Click **"Upload"**
7. Wait 5-15 minutes
8. You'll get email: "The build has been uploaded"

---

## STEP 9: Create App Store Listing

### Go to App Store Connect

1. Visit: https://appstoreconnect.apple.com
2. Sign in with Apple ID
3. Click **"My Apps"**

### Create New App

1. Click **"+"** button > **"New App"**
2. Fill in:

```
Platform: iOS
Name: Text to SQL
Primary Language: English (U.S.)
Bundle ID: com.jayyvora.texttosql (select from dropdown)
SKU: texttosql001
User Access: Full Access
```

3. Click **"Create"**

### Fill in App Information

#### App Information Tab

**Category:**
- Primary: Education
- Secondary: Productivity

**Age Rating:**
- Click "Edit"
- Answer all questions (all "No" for this app)
- Rated: 4+

#### Pricing and Availability

- **Price:** Free (0.00)
- **Availability:** All countries

#### App Privacy

Click "Get Started":

1. **Do you collect data?** Choose based on your app:
   - If using Hugging Face only: Minimal or No
   - Add: "User queries sent to Hugging Face for processing"

2. **Data Types:** None (or Analytics if you add analytics)

3. Save privacy settings

### Add Version Information

Go to your app > **1.0 Prepare for Submission**

#### App Information

**Description** (4000 chars max):

```
Text to SQL - Natural Language Database Queries

Transform plain English questions into SQL queries instantly! Perfect for students, educators, and anyone exploring databases without coding.

✨ FEATURES
• Ask questions in natural language
• Instant SQL query generation
• View results in real-time
• Educational student grades database
• Powered by AI (Llama 3)
• No coding knowledge required

🎯 PERFECT FOR
• Students learning SQL and databases
• Teachers demonstrating query concepts
• Data analysts exploring data
• Anyone curious about databases

💬 TRY THESE QUESTIONS
- "Who got the highest score in Mathematics?"
- "Show all students with grade A"
- "What is the average score for each subject?"
- "List all grades for Alice Johnson"
- "Who are the top 3 students?"

🎓 LEARN SQL NATURALLY
See how your questions become SQL queries. Learn SQL syntax by example as you explore the database.

🔒 PRIVACY & SECURITY
Your queries are processed securely through Hugging Face Spaces. No personal data is collected or stored permanently.

🤖 AI-POWERED
Built with advanced language AI (Llama 3) running locally on Hugging Face for accurate, context-aware SQL generation.

Whether you're a student, teacher, or data enthusiast, Text to SQL makes database queries accessible and educational!
```

**Keywords** (100 chars max):
```
sql,database,query,ai,education,nlp,student,text-to-sql,llama
```

**Support URL:**
```
https://github.com/jvora89-cloud/text-to-sql-app
```

**Marketing URL** (optional):
```
https://github.com/jvora89-cloud/text-to-sql-app
```

**Privacy Policy URL:**
```
[YOUR PRIVACY POLICY URL FROM STEP 6]
```

#### Media Assets

**App Previews and Screenshots**

1. Select **6.7" Display** (iPhone 15 Pro Max)
2. Click **"+"** to add screenshots
3. Upload your 5 screenshots from Step 5
4. Drag to reorder if needed

**Order:**
1. Home screen
2. Entering query
3. Generated SQL
4. Results
5. Different example

#### Build

1. Scroll down to **"Build"** section
2. Click **"+"** Add Build
3. Select your uploaded build (may take 10-30 min to appear)
4. If not there, wait and refresh

**If build doesn't appear:**
- Check email for processing errors
- Go to TestFlight tab to see if it's still processing

#### Version Information

**Copyright:**
```
2026 Jay Vora
```

**Routing App Coverage File:** Leave empty

#### App Review Information

**Contact Information:**
- First Name: Jay
- Last Name: Vora
- Phone: [Your phone number]
- Email: [Your email]

**Demo Account:** Not needed

**Notes:**
```
This app connects to a Hugging Face Space backend at:
https://jayyvora-text-to-sql-app.hf.space

The backend must be running for the app to function. No login required. Simply open the app and start asking questions about the student grades database.

Test questions:
- "Who got the highest score in Mathematics?"
- "Show all students with grade A"
```

**Attachments:** None needed

---

## STEP 10: Submit for Review

### Final Checks

- [ ] All fields completed (no yellow warnings)
- [ ] Build is selected
- [ ] Screenshots uploaded (5 minimum)
- [ ] Privacy policy URL added
- [ ] Description looks good
- [ ] Hugging Face Space is running ✅

### Submit

1. Click **"Save"** at top right
2. Click **"Submit for Review"** button
3. Confirm submission
4. You'll see: **"Waiting for Review"**

---

## STEP 11: Wait for Review

### Timeline

- **In Review:** 1-3 days (usually 24-48 hours)
- **Review Time:** Few hours
- **Total:** 2-4 days typically

### You'll Get Emails

1. **"Your app status is In Review"** - Apple is testing
2. **"Your app status is Ready for Sale"** - APPROVED! 🎉

### If Rejected

- Read rejection reason carefully
- Fix the issue
- Submit again (usually approved 2nd time)

---

## STEP 12: Launch! 🚀

### Once Approved

- App automatically goes live
- Appears in App Store within hours
- Download link: Search "Text to SQL" in App Store

### Share Your App

Get your App Store link:
```
https://apps.apple.com/app/id[YOUR_APP_ID]
```

Share on:
- Social media
- GitHub README
- Friends and family

---

## 📊 After Launch

### Monitor Your App

**App Store Connect:**
- View downloads
- Check ratings and reviews
- See crash reports

**Respond to Reviews:**
- Reply to user feedback
- Fix bugs in updates

### Future Updates

To update your app:

1. Make changes to code
2. Increment version number (1.0.0 → 1.0.1)
3. Archive and upload new build
4. Add "What's New" in App Store Connect
5. Submit for review again

---

## 🆘 Troubleshooting

### "No Signing Identity Found"
**Fix:** Add Apple Developer account in Xcode > Settings > Accounts

### "Archive Failed"
**Fix:** Product > Clean Build Folder, then try again

### "Build Not Appearing in App Store Connect"
**Fix:** Wait 30 minutes, check TestFlight tab for processing

### "App Crashes on Launch"
**Fix:** Test in simulator first, check console for errors

### "Rejection: App Not Functional"
**Fix:** Ensure Hugging Face Space is running and accessible

---

## ✅ Quick Checklist

Before submitting, verify:

- [ ] Apple Developer account active
- [ ] App builds and runs in Xcode
- [ ] App icons added (all sizes)
- [ ] 5+ screenshots taken
- [ ] Privacy policy URL created
- [ ] Archive uploaded successfully
- [ ] App Store listing complete
- [ ] Build selected in App Store Connect
- [ ] Hugging Face Space running
- [ ] Contact info provided
- [ ] Submitted for review

---

## 🎉 Success!

**Your app will be on the App Store in 2-4 days!**

Once approved, anyone can download "Text to SQL" and start querying databases with natural language!

**Congratulations! 🚀📱**

---

## 📞 Need Help?

- **Apple Developer Support:** https://developer.apple.com/support/
- **Xcode Help:** Help menu > Xcode Help
- **App Store Review Guidelines:** https://developer.apple.com/app-store/review/guidelines/
