# 🎸 אקורד — מדריך פרסום ב-Google Play

## מה כבר מוכן בתיקייה זו
- ✅ `index.html` — מעודכן עם safe-area לאנדרואיד
- ✅ `capacitor.config.json` — הגדרות Capacitor
- ✅ `package.json` — עם כל התלויות
- ✅ `privacy-policy.html` — מדיניות פרטיות (נדרש ל-Google Play)
- ✅ `android-permissions.xml` — ההרשאות להוסיף ל-AndroidManifest

---

## שלב 0 — דבר אחד לפני הכל ⚠️

פתח את `index.html` וחפש:
```
https://YOUR-NETLIFY-SITE.netlify.app/api/coach
```
החלף את `YOUR-NETLIFY-SITE` בשם האתר שלך ב-Netlify.
(למשל: `https://akord-guitar.netlify.app/api/coach`)

---

## שלב 1 — התקנות נדרשות (רק פעם אחת)

### 1.1 Java JDK 17
- **Mac:** `brew install openjdk@17`
- **Windows:** הורד מ-https://adoptium.net

### 1.2 Android Studio
הורד מ-https://developer.android.com/studio
(כולל Android SDK באופן אוטומטי)

### 1.3 Node.js 18+
הורד מ-https://nodejs.org (בחר גרסת LTS)

---

## שלב 2 — הגדרת Capacitor

פתח טרמינל בתיקיית הפרויקט:

```bash
# התקן את כל החבילות
npm install

# סנכרן קבצים
npx cap sync android
```

---

## שלב 3 — הוספת הרשאות Android

לאחר `npm install`, פתח את הקובץ:
```
android/app/src/main/AndroidManifest.xml
```

הוסף את השורות הבאות **לפני** `<application`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

---

## שלב 4 — פתח ב-Android Studio

```bash
npx cap open android
```

Android Studio ייפתח עם הפרויקט.

### הוסף אייקון לאפליקציה
1. ב-Android Studio: קליק ימני על `app` > `New` > `Image Asset`
2. בחר `Launcher Icons`
3. העלה תמונה מרובעת (מינימום 1024×1024 px) עם הלוגו של אקורד
4. לחץ `Next` > `Finish`

---

## שלב 5 — בנה AAB לחתימה

1. ב-Android Studio: `Build` > `Generate Signed Bundle / APK`
2. בחר `Android App Bundle` > `Next`
3. צור Keystore חדש:
   - לחץ `Create new...`
   - בחר מיקום לשמירה (חשוב! שמור את הקובץ במקום בטוח)
   - מלא: Key alias = `akord-key`, תוקף = 25 שנה
   - מלא סיסמה חזקה
4. בחר `release` > `Finish`
5. הקובץ ייווצר ב: `android/app/release/app-release.aab`

> ⚠️ **חשוב:** שמור את קובץ ה-Keystore ואת הסיסמאות שלו!
> בלעדיהם לא תוכל לעדכן את האפליקציה בעתיד.

---

## שלב 6 — פרסום ב-Google Play

### 6.1 צור חשבון Google Play Console
1. כנס ל-https://play.google.com/console
2. שלם $25 (חד-פעמי)
3. אמת פרטי זהות

### 6.2 צור אפליקציה חדשה
- שם: `אקורד – לימוד גיטרה`
- שפה ברירת מחדל: עברית (he)
- סוג: App
- קטגוריה: Education

### 6.3 מלא את הפרטים הנדרשים

**Store Listing:**
- כותרת: `אקורד – לימוד גיטרה בעברית`
- תיאור קצר (80 תווים): `למד לנגן גיטרה בעברית עם מאמן AI, שיעורים ושירים ישראליים`
- תיאור מלא: (ראה בהמשך)
- צילומי מסך: מינימום 2 (מחייב)
- אייקון: 512×512 px

**Content Rating:**
- מלא את השאלון, בחר Everyone / 4+

**Privacy Policy:**
- העלה את `privacy-policy.html` ל-Netlify שלך
- הכנס את ה-URL בשדה Privacy Policy

### 6.4 העלה את ה-AAB
1. `Production` > `Create new release`
2. העלה את `app-release.aab`
3. מלא הערות גרסה (release notes)
4. `Save` > `Review release` > `Start rollout`

### 6.5 המתן לאישור
בדרך כלל 1-3 ימי עסקים.

---

## תיאור מלא לחנות (העתק-הדבק)

```
🎸 אקורד — לימוד גיטרה בעברית, עם מאמן AI חכם

ללמוד גיטרה מאפס, בעברית, בקצב שלך — עם שיעורים מובנים, שירים ישראליים אמיתיים, וכוונן מקצועי.

✨ מה תקבל:
• 11 שיעורים שלב-אחר-שלב, מאקורד Em הראשון ועד נגינת שירים שלמים
• שירים ישראליים קלאסיים: התקווה, הבה נגילה, מעוז צור ועוד
• מאמן AI שעונה על כל שאלה בעברית, בכל שעה
• כוונן גיטרה מובנה עם זיהוי צליל בזמן אמת
• מערכת הישגים ורצף ימים (streak) שמשאירה אותך ממוקד

🎵 למי זה מתאים?
למתחילים מוחלטים — לא נדרש ניסיון קודם.

📵 אפשרי גם ללא הרשמה
שחק ולמד מיד, ללא צורך בחשבון. ההרשמה מאפשרת שמירת התקדמות.

אפליקציה לסימולציה ולמידה בלבד.
```

---

## עדכונים עתידיים

לעדכן את האפליקציה בחנות:
1. ערוך את הקוד
2. `npx cap sync android`
3. עדכן `versionCode` ו-`versionName` ב-`android/app/build.gradle`
4. בנה AAB חדש עם אותו Keystore
5. העלה ב-Play Console

---

## עזרה נוספת

שלח לי שאלה בצ'אט ואעזור עם כל שלב! 🚀
