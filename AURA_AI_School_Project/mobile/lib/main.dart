import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:flutter_tts/flutter_tts.dart';

const String apiBaseUrl = String.fromEnvironment(
  'AURA_API_URL',
  defaultValue: 'https://aura-ai-mkc2.onrender.com',
);

void main() => runApp(const AuraApp());

class AuraApp extends StatelessWidget {
  const AuraApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'AURA AI',
      theme: ThemeData.dark(useMaterial3: true).copyWith(
        scaffoldBackgroundColor: const Color(0xFF050713),
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF665CFF)),
      ),
      home: const AuraHome(),
    );
  }
}

class AuraHome extends StatefulWidget {
  const AuraHome({super.key});

  @override
  State<AuraHome> createState() => _AuraHomeState();
}

class _AuraHomeState extends State<AuraHome>
    with SingleTickerProviderStateMixin {
  final TextEditingController controller = TextEditingController();
  final ScrollController scroll = ScrollController();
  final stt.SpeechToText speech = stt.SpeechToText();
  final FlutterTts tts = FlutterTts();

  final List<Map<String, String>> messages = [
    {
      'role': 'ai',
      'text': "Hey! 👋 I'm AURA AI.\nYou can type or speak naturally."
    }
  ];

  late AnimationController pulse;

  bool listening = false;
  bool thinking = false;
  bool speaking = false;
  bool chatVisible = true;
  bool speechReady = false;

  @override
  void initState() {
    super.initState();
    pulse = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1100),
      lowerBound: 0.92,
      upperBound: 1.08,
    )..repeat(reverse: true);

    _setupSpeech();
  }

  Future<void> _setupSpeech() async {
    speechReady = await speech.initialize(
      onStatus: (status) {
        if (status == 'done' && !thinking && !speaking) {
          _startListening();
        }
      },
      onError: (_) {
        if (mounted) setState(() => listening = false);
      },
    );
    if (speechReady && mounted) {
      setState(() {});
      _startListening();
    }
  }

  Future<void> _startListening() async {
    if (!speechReady || thinking || speaking || listening) return;

    setState(() => listening = true);

    await speech.listen(
      localeId: 'en_IN',
      listenMode: stt.ListenMode.confirmation,
      onResult: (result) {
        if (result.finalResult) {
          final text = result.recognizedWords.trim();
          speech.stop();
          if (text.isNotEmpty) _send(text);
        }
      },
    );
  }

  Future<void> _send([String? value]) async {
    if (thinking) return;

    final text = (value ?? controller.text).trim();
    if (text.isEmpty) return;

    controller.clear();
    await speech.stop();

    setState(() {
      listening = false;
      thinking = true;
      messages.add({'role': 'user', 'text': text});
    });
    _scrollBottom();

    try {
      final response = await http.post(
        Uri.parse('$apiBaseUrl/api/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'message': text}),
      );

      final data = jsonDecode(response.body) as Map<String, dynamic>;
      final reply = (data['reply'] ?? 'Sorry, no response.').toString();

      if (!mounted) return;
      setState(() {
        thinking = false;
        messages.add({'role': 'ai', 'text': reply});
      });
      _scrollBottom();
      await _speak(reply);
    } catch (_) {
      if (!mounted) return;
      setState(() {
        thinking = false;
        messages.add({
          'role': 'ai',
          'text': 'Sorry, AURA AI could not connect right now.'
        });
      });
      _scrollBottom();
      _startListening();
    }
  }

  Future<void> _speak(String text) async {
    speaking = true;
    if (mounted) setState(() {});
    final isHindi = RegExp(r'[\u0900-\u097F]').hasMatch(text);

    await tts.setLanguage(isHindi ? 'hi-IN' : 'en-IN');
    await tts.setSpeechRate(0.48);
    await tts.setPitch(1.0);

    await tts.speak(text);
    await Future.delayed(const Duration(milliseconds: 300));

    speaking = false;
    if (mounted) setState(() {});
    _startListening();
  }

  void _scrollBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (scroll.hasClients) {
        scroll.animateTo(
          scroll.position.maxScrollExtent,
          duration: const Duration(milliseconds: 250),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    pulse.dispose();
    controller.dispose();
    scroll.dispose();
    speech.stop();
    tts.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final orbScale =
        (listening || thinking || speaking) ? pulse : const AlwaysStoppedAnimation(1.0);

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xCC050713),
        title: Row(
          children: [
            const Icon(Icons.auto_awesome, color: Color(0xFF8A7CFF)),
            const SizedBox(width: 10),
            const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('AURA AI', style: TextStyle(fontWeight: FontWeight.bold)),
                Text('YOUR AI ASSISTANT',
                    style: TextStyle(fontSize: 9, color: Colors.grey)),
              ],
            ),
          ],
        ),
        actions: [
          IconButton(
            tooltip: chatVisible ? 'Hide chat' : 'Show chat',
            onPressed: () => setState(() => chatVisible = !chatVisible),
            icon: Icon(chatVisible ? Icons.close : Icons.chat_bubble_outline),
          ),
        ],
      ),
      body: Stack(
        children: [
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ScaleTransition(
                  scale: orbScale,
                  child: Container(
                    width: 190,
                    height: 190,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      gradient: const RadialGradient(
                        colors: [
                          Colors.white,
                          Color(0xFF8D80FF),
                          Color(0xFF3426A0),
                          Color(0xFF090B1A),
                        ],
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: speaking
                              ? Colors.cyanAccent
                              : const Color(0xFF665CFF),
                          blurRadius: 50,
                          spreadRadius: 8,
                        ),
                      ],
                    ),
                    alignment: Alignment.center,
                    child: const Text(
                      'AURA',
                      style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.w900,
                        letterSpacing: 4,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 36),
                Text(
                  speaking
                      ? 'AURA is speaking...'
                      : thinking
                          ? 'Thinking...'
                          : listening
                              ? 'Listening...'
                              : 'Ready',
                  style: const TextStyle(fontSize: 17, color: Color(0xFFBEC2E2)),
                ),
                const SizedBox(height: 8),
                const Text(
                  'Speak naturally — AURA listens automatically',
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                ),
                const SizedBox(height: 18),
                const Text(
                  'Made by JLPG',
                  style: TextStyle(fontSize: 11, color: Colors.grey),
                ),
              ],
            ),
          ),

          if (chatVisible)
            Align(
              alignment: Alignment.bottomCenter,
              child: SafeArea(
                child: Container(
                  height: MediaQuery.of(context).size.height * 0.44,
                  margin: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: const Color(0xF20A0C1C),
                    borderRadius: BorderRadius.circular(18),
                    border: Border.all(color: Colors.white12),
                  ),
                  child: Column(
                    children: [
                      const Padding(
                        padding: EdgeInsets.all(13),
                        child: Align(
                          alignment: Alignment.centerLeft,
                          child: Text(
                            'AURA CHAT',
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                        ),
                      ),
                      Expanded(
                        child: ListView.builder(
                          controller: scroll,
                          padding: const EdgeInsets.symmetric(horizontal: 12),
                          itemCount: messages.length,
                          itemBuilder: (_, index) {
                            final item = messages[index];
                            final user = item['role'] == 'user';
                            return Align(
                              alignment:
                                  user ? Alignment.centerRight : Alignment.centerLeft,
                              child: Container(
                                constraints: const BoxConstraints(maxWidth: 330),
                                margin: const EdgeInsets.only(bottom: 9),
                                padding: const EdgeInsets.all(11),
                                decoration: BoxDecoration(
                                  color: user
                                      ? const Color(0xFF5B4DDB)
                                      : Colors.white10,
                                  borderRadius: BorderRadius.circular(13),
                                ),
                                child: Text(item['text'] ?? ''),
                              ),
                            );
                          },
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.fromLTRB(10, 5, 10, 10),
                        child: Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: controller,
                                onSubmitted: (_) => _send(),
                                decoration: InputDecoration(
                                  hintText: 'Type a message...',
                                  filled: true,
                                  fillColor: Colors.white10,
                                  border: OutlineInputBorder(
                                    borderRadius: BorderRadius.circular(11),
                                    borderSide: BorderSide.none,
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(width: 8),
                            IconButton.filled(
                              onPressed: thinking ? null : () => _send(),
                              icon: const Icon(Icons.send),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
