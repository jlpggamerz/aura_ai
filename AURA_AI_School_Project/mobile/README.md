# AURA AI Mobile

This folder contains the Flutter source for Android and iOS.

## 1. Install Flutter

Install Flutter on your development computer, then verify:

```bash
flutter doctor
```

## 2. Create the platform folders

From this directory:

```bash
flutter create .
```

This generates the standard `android/` and `ios/` folders while keeping the Dart/pubspec files.

## 3. Install packages

```bash
flutter pub get
```

## 4. Run

Android:

```bash
flutter run
```

iOS (requires macOS + Xcode):

```bash
flutter run
```

## 5. Point the app to your Render backend

Default URL in `lib/main.dart` is:

https://aura-ai-mkc2.onrender.com

Or use another backend:

```bash
flutter run --dart-define=AURA_API_URL=https://your-domain.example
```

## Android microphone permission

`android/app/src/main/AndroidManifest.xml` should contain:

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO"/>
<uses-permission android:name="android.permission.INTERNET"/>
```

## iOS microphone/speech permissions

In `ios/Runner/Info.plist`, add:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>AURA AI uses the microphone for voice conversations.</string>
<key>NSSpeechRecognitionUsageDescription</key>
<string>AURA AI uses speech recognition for voice conversations.</string>
```
