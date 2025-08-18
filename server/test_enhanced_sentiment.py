from utils.enhanced_sentiment import EnhancedEmotionAnalyzer
import json

def test_enhanced_sentiment_detailed():
    """Detailed testing showing every step of the enhanced sentiment analysis"""
    
    print("🧪 DETAILED ENHANCED SENTIMENT ANALYSIS - STEP BY STEP")
    print("=" * 80)
    
    analyzer = EnhancedEmotionAnalyzer()
    
    # Test cases covering different emotional scenarios
    test_cases = [
        "I'm so happy about my new job!",
        "I'm feeling really anxious about my upcoming presentation",
        "I'm sad because I had a fight with my best friend",
        "I'm absolutely furious with my roommate right now!",
        "I'm kind of worried about my health",
        "I'm not happy with how things are going",
        "I'm feeling hopeless and don't know what to do anymore",
        "I'm excited but also nervous about the future",
        "I'm really confused about my feelings",
        "I'm feeling great today!"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"📝 TEST {i}: '{test_text}'")
        print(f"{'='*80}")
        
        try:
            # Step 1: Basic VADER Sentiment Analysis
            print("\n🔍 STEP 1: BASIC VADER SENTIMENT ANALYSIS")
            print("-" * 50)
            vader_scores = analyzer.vader.polarity_scores(test_text)
            print(f"   Positive Score: {vader_scores['pos']:.3f}")
            print(f"   Negative Score: {vader_scores['neg']:.3f}")
            print(f"   Neutral Score: {vader_scores['neu']:.3f}")
            print(f"   Compound Score: {vader_scores['compound']:.3f}")
            
            # Step 2: Enhanced Emotion Detection
            print("\n🎭 STEP 2: ENHANCED EMOTION DETECTION")
            print("-" * 50)
            emotion_scores = analyzer._detect_emotions(test_text)
            print("   Raw Emotion Scores:")
            for emotion, score in sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True):
                if score > 0:
                    print(f"      {emotion}: {score:.1f}")
            
            # Step 3: Crisis Detection
            print("\n�� STEP 3: CRISIS DETECTION")
            print("-" * 50)
            crisis_level = analyzer._detect_crisis(test_text)
            print(f"   Crisis Level: {crisis_level['level']:.3f}")
            print(f"   Risk Category: {crisis_level['risk_category']}")
            print(f"   Needs Immediate Attention: {crisis_level['needs_immediate_attention']}")
            if crisis_level['indicators']:
                print(f"   Crisis Indicators: {', '.join(crisis_level['indicators'])}")
            
            # Step 4: Context Analysis
            print("\n🏷️  STEP 4: CONTEXT ANALYSIS")
            print("-" * 50)
            context_info = analyzer._analyze_context(test_text)
            print(f"   Primary Topic: {context_info['primary_topic']}")
            print(f"   Detected Topics:")
            for topic, score in context_info['topics'].items():
                print(f"      {topic}: {score}")
            print(f"   Emotional Context: {context_info['emotional_context']}")
            
            # Step 5: Linguistic Pattern Analysis
            print("\n�� STEP 5: LINGUISTIC PATTERN ANALYSIS")
            print("-" * 50)
            linguistic_patterns = analyzer._analyze_linguistic_patterns(test_text)
            if linguistic_patterns:
                for pattern, value in linguistic_patterns.items():
                    print(f"   {pattern}: {value:.3f}")
            else:
                print("   No significant linguistic patterns detected")
            
            # Step 6: Combined Analysis
            print("\n🧠 STEP 6: COMBINED ANALYSIS")
            print("-" * 50)
            overall_analysis = analyzer._combine_analysis(
                vader_scores, emotion_scores, crisis_level, context_info, linguistic_patterns
            )
            print(f"   Primary Emotion: {overall_analysis['primary_emotion']}")
            print(f"   Intensity: {overall_analysis['intensity']}")
            print(f"   Support Strategy: {overall_analysis['support_strategy']}")
            print(f"   Emotional Complexity: {overall_analysis['emotional_complexity']}")
            print(f"   Emotional State: {overall_analysis['emotional_state']}")
            
            # Step 7: Confidence Calculation
            print("\n�� STEP 7: CONFIDENCE CALCULATION")
            print("-" * 50)
            confidence = analyzer._calculate_confidence(vader_scores, emotion_scores, linguistic_patterns)
            print(f"   Overall Confidence: {confidence['overall']:.3f}")
            print(f"   VADER Confidence: {confidence['vader']:.3f}")
            print(f"   Emotion Detection Confidence: {confidence['emotion_detection']:.3f}")
            print(f"   Linguistic Patterns Confidence: {confidence['linguistic_patterns']:.3f}")
            
            # Step 8: Final Complete Analysis
            print("\n�� STEP 8: FINAL COMPLETE ANALYSIS")
            print("-" * 50)
            complete_analysis = analyzer.analyze_emotion(test_text)
            
            print("   📊 COMPLETE RESULTS:")
            print(f"      Basic Sentiment: {complete_analysis['basic_sentiment']}")
            print(f"      Emotions: {dict(list(complete_analysis['emotions'].items())[:5])}")  # Top 5
            print(f"      Crisis Level: {complete_analysis['crisis_level']}")
            print(f"      Context: {complete_analysis['context']}")
            print(f"      Linguistic Patterns: {complete_analysis['linguistic_patterns']}")
            print(f"      Overall Analysis: {complete_analysis['overall_analysis']}")
            print(f"      Confidence: {complete_analysis['confidence']}")
            
            # Step 9: Raw Data Export (Optional)
            print("\n💾 STEP 9: RAW DATA EXPORT")
            print("-" * 50)
            print("   Raw JSON data (first 500 chars):")
            json_str = json.dumps(complete_analysis, indent=2)
            print(f"   {json_str[:500]}...")
            
        except Exception as e:
            print(f"   ❌ Error during analysis: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"\n{'='*80}")
        print(f"✅ TEST {i} COMPLETED")
        print(f"{'='*80}")
        
        # Small separator between tests for readability
        print("\n" + "─" * 80 + "\n")

def test_specific_components():
    """Test individual components in detail"""
    
    print("\n�� TESTING INDIVIDUAL COMPONENTS")
    print("=" * 80)
    
    analyzer = EnhancedEmotionAnalyzer()
    test_text = "I'm feeling really anxious about my upcoming presentation"
    
    print(f"Test Text: '{test_text}'")
    print("-" * 50)
    
    # Test emotion keywords
    print("\n📚 EMOTION KEYWORDS TEST:")
    emotion_keywords = analyzer._load_emotion_keywords()
    for emotion, keywords in emotion_keywords.items():
        found_keywords = [kw for kw in keywords if kw in test_text.lower()]
        if found_keywords:
            print(f"   {emotion}: {found_keywords}")
    
    # Test crisis keywords
    print("\n🚨 CRISIS KEYWORDS TEST:")
    crisis_keywords = analyzer._load_crisis_keywords()
    found_crisis = [kw for kw in crisis_keywords if kw in test_text.lower()]
    if found_crisis:
        print(f"   Found crisis keywords: {found_crisis}")
    else:
        print("   No crisis keywords found")
    
    # Test intensity modifiers
    print("\n⚡ INTENSITY MODIFIERS TEST:")
    intensity_modifiers = analyzer._load_intensity_modifiers()
    for modifier_type, modifiers in intensity_modifiers.items():
        found_modifiers = [mod for mod in modifiers if mod in test_text.lower()]
        if found_modifiers:
            print(f"   {modifier_type}: {found_modifiers}")

if __name__ == "__main__":
    print("Choose testing mode:")
    print("1. Full step-by-step analysis (no prompts)")
    print("2. Individual component testing")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_enhanced_sentiment_detailed()
    elif choice == "2":
        test_specific_components()
    else:
        print("Invalid choice. Running full analysis...")
        test_enhanced_sentiment_detailed() 