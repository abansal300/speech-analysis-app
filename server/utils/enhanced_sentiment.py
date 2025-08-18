import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import re
from collections import Counter
import os

class EnhancedEmotionAnalyzer:
    def __init__(self):
        """Initialize the enhanced emotion analyzer with NLTK data"""
        self._download_nltk_data()
        self.vader = SentimentIntensityAnalyzer()
        self.emotion_keywords = self._load_emotion_keywords()
        self.crisis_keywords = self._load_crisis_keywords()
        self.intensity_modifiers = self._load_intensity_modifiers()
    
    def _download_nltk_data(self):
        """Download required NLTK data packages"""
        try:
            # Download punkt tokenizer
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt')
        
        try:
            # Download stopwords
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("Downloading NLTK stopwords...")
            nltk.download('stopwords')
        
        try:
            # Download averaged_perceptron_tagger for POS tagging
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            print("Downloading NLTK POS tagger...")
            nltk.download('averaged_perceptron_tagger')
        
        try:
            # Download VADER lexicon (this was missing!)
            nltk.data.find('sentiment/vader_lexicon')
        except LookupError:
            print("Downloading NLTK VADER lexicon...")
            nltk.download('vader_lexicon')
    
    def analyze_emotion(self, text):
        """
        Comprehensive emotional analysis using multiple techniques
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Comprehensive emotional analysis results
        """
        if not text or not text.strip():
            return self._empty_analysis()
        
        # Basic VADER sentiment
        vader_scores = self.vader.polarity_scores(text)
        
        # Enhanced emotion detection
        emotion_scores = self._detect_emotions(text)
        
        # Crisis detection
        crisis_level = self._detect_crisis(text)
        
        # Context analysis
        context_info = self._analyze_context(text)
        
        # Linguistic pattern analysis
        linguistic_patterns = self._analyze_linguistic_patterns(text)
        
        # Combine all analyses
        overall_analysis = self._combine_analysis(
            vader_scores, emotion_scores, crisis_level, context_info, linguistic_patterns
        )
        
        return {
            'basic_sentiment': vader_scores,
            'emotions': emotion_scores,
            'crisis_level': crisis_level,
            'context': context_info,
            'linguistic_patterns': linguistic_patterns,
            'overall_analysis': overall_analysis,
            'confidence': self._calculate_confidence(vader_scores, emotion_scores, linguistic_patterns)
        }
    
    def _detect_emotions(self, text):
        """
        Detect specific emotions using keyword analysis and linguistic patterns
        """
        text_lower = text.lower()
        tokens = word_tokenize(text_lower)
        
        # Initialize emotion scores
        emotion_scores = {
            'joy': 0, 'sadness': 0, 'anger': 0, 'fear': 0, 
            'surprise': 0, 'disgust': 0, 'trust': 0, 'anticipation': 0,
            'love': 0, 'confusion': 0, 'excitement': 0, 'worry': 0
        }
        
        # Count emotion keywords
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    emotion_scores[emotion] += 1
        
        # Analyze emotional intensity modifiers
        emotion_scores = self._apply_intensity_modifiers(text_lower, emotion_scores)
        
        # Analyze negation (e.g., "not happy" should decrease joy)
        emotion_scores = self._analyze_negation(text_lower, emotion_scores)
        
        return emotion_scores
    
    def _apply_intensity_modifiers(self, text_lower, emotion_scores):
        """
        Apply intensity modifiers to emotion scores
        """
        # Very, really, extremely, etc. increase intensity
        intensifiers = ['very', 'really', 'extremely', 'incredibly', 'absolutely', 'totally']
        for intensifier in intensifiers:
            if intensifier in text_lower:
                # Find the emotion word that follows
                words = text_lower.split()
                for i, word in enumerate(words):
                    if word == intensifier and i + 1 < len(words):
                        next_word = words[i + 1]
                        for emotion, keywords in self.emotion_keywords.items():
                            if next_word in keywords:
                                emotion_scores[emotion] += 0.5
        
        # Slightly, kind of, etc. decrease intensity
        deintensifiers = ['slightly', 'kind of', 'sort of', 'a little', 'somewhat']
        for deintensifier in deintensifiers:
            if deintensifier in text_lower:
                words = text_lower.split()
                for i, word in enumerate(words):
                    if word in deintensifiers and i + 1 < len(words):
                        next_word = words[i + 1]
                        for emotion, keywords in self.emotion_keywords.items():
                            if next_word in keywords:
                                emotion_scores[emotion] = max(0, emotion_scores[emotion] - 0.3)
        
        return emotion_scores
    
    def _analyze_negation(self, text_lower, emotion_scores):
        """
        Analyze negation to adjust emotion scores
        """
        negations = ['not', 'no', 'never', 'none', 'neither', 'nor']
        
        for negation in negations:
            if negation in text_lower:
                words = text_lower.split()
                for i, word in enumerate(words):
                    if word in negations and i + 1 < len(words):
                        next_word = words[i + 1]
                        for emotion, keywords in self.emotion_keywords.items():
                            if next_word in keywords:
                                # Reduce the positive emotion or increase the opposite
                                if emotion in ['joy', 'trust', 'anticipation']:
                                    emotion_scores[emotion] = max(0, emotion_scores[emotion] - 1)
                                    if emotion == 'joy':
                                        emotion_scores['sadness'] += 0.5
                                    elif emotion == 'trust':
                                        emotion_scores['fear'] += 0.5
                                elif emotion in ['fear', 'sadness']:
                                    emotion_scores[emotion] = max(0, emotion_scores[emotion] - 1)
                                    if emotion == 'fear':
                                        emotion_scores['trust'] += 0.5
                                    elif emotion == 'sadness':
                                        emotion_scores['joy'] += 0.5
        
        return emotion_scores
    
    def _analyze_linguistic_patterns(self, text):
        """
        Analyze linguistic patterns that indicate emotions
        """
        patterns = {}
        
        # Exclamation marks (excitement, anger, surprise)
        exclamation_count = text.count('!')
        if exclamation_count > 0:
            patterns['excitement'] = min(exclamation_count * 0.3, 1.0)
        
        # Question marks (uncertainty, curiosity, confusion)
        question_count = text.count('?')
        if question_count > 0:
            patterns['uncertainty'] = min(question_count * 0.2, 1.0)
            patterns['curiosity'] = min(question_count * 0.15, 1.0)
        
        # Capitalization (emphasis, strong emotion)
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        if caps_ratio > 0.3:
            patterns['intensity'] = min(caps_ratio, 1.0)
            patterns['emphasis'] = min(caps_ratio * 0.8, 1.0)
        
        # Repeated words (emphasis, strong feeling)
        tokens = word_tokenize(text.lower())
        word_freq = Counter(tokens)
        repeated_words = sum(1 for word, count in word_freq.items() if count > 1)
        if repeated_words > 0:
            patterns['emphasis'] = min(repeated_words * 0.1, 1.0)
        
        # Ellipsis (uncertainty, trailing off)
        ellipsis_count = text.count('...')
        if ellipsis_count > 0:
            patterns['uncertainty'] = min(patterns.get('uncertainty', 0) + ellipsis_count * 0.2, 1.0)
            patterns['trailing_off'] = min(ellipsis_count * 0.3, 1.0)
        
        return patterns
    
    def _detect_crisis(self, text):
        """
        Detect crisis situations that need immediate attention
        """
        text_lower = text.lower()
        crisis_score = 0
        crisis_indicators = []
        
        # Check for crisis keywords
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                crisis_score += 0.3
                crisis_indicators.append(keyword)
        
        # Check for extreme language
        extreme_words = ['never', 'always', 'hate', 'despise', 'terrible', 'horrible', 'awful']
        for word in extreme_words:
            if word in text_lower:
                crisis_score += 0.1
        
        # Check for hopelessness
        hopeless_phrases = ['give up', 'no point', 'nothing matters', 'end it all', 'can\'t take it']
        for phrase in hopeless_phrases:
            if phrase in text_lower:
                crisis_score += 0.4
        
        # Check for isolation
        isolation_phrases = ['no one cares', 'alone', 'nobody understands', 'no one gets it']
        for phrase in isolation_phrases:
            if phrase in text_lower:
                crisis_score += 0.2
        
        return {
            'level': min(crisis_score, 1.0),
            'indicators': crisis_indicators,
            'needs_immediate_attention': crisis_score > 0.7,
            'risk_category': self._categorize_crisis_risk(crisis_score)
        }
    
    def _categorize_crisis_risk(self, crisis_score):
        """
        Categorize the level of crisis risk
        """
        if crisis_score > 0.8:
            return 'critical'
        elif crisis_score > 0.6:
            return 'high'
        elif crisis_score > 0.4:
            return 'moderate'
        elif crisis_score > 0.2:
            return 'low'
        else:
            return 'none'
    
    def _analyze_context(self, text):
        """
        Analyze the context and topics being discussed
        """
        text_lower = text.lower()
        
        # Topic detection with weighted scoring
        topics = {
            'work': ['work', 'job', 'career', 'boss', 'colleague', 'presentation', 'deadline', 'meeting', 'project'],
            'relationships': ['family', 'friend', 'partner', 'relationship', 'love', 'breakup', 'marriage', 'dating'],
            'health': ['health', 'sick', 'pain', 'doctor', 'hospital', 'medication', 'symptoms', 'treatment'],
            'education': ['school', 'college', 'exam', 'study', 'homework', 'grade', 'class', 'assignment'],
            'personal': ['goal', 'dream', 'future', 'past', 'memory', 'achievement', 'hobby', 'interest'],
            'financial': ['money', 'bills', 'debt', 'salary', 'expenses', 'budget', 'financial'],
            'social': ['party', 'social', 'group', 'crowd', 'people', 'conversation', 'interaction']
        }
        
        detected_topics = {}
        for topic, keywords in topics.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                detected_topics[topic] = score
        
        # Determine primary topic
        primary_topic = max(detected_topics.items(), key=lambda x: x[1])[0] if detected_topics else 'general'
        
        # Analyze emotional context (how the topic relates to emotions)
        emotional_context = self._analyze_emotional_context(text_lower, primary_topic)
        
        return {
            'topics': detected_topics,
            'primary_topic': primary_topic,
            'emotional_context': emotional_context
        }
    
    def _analyze_emotional_context(self, text_lower, primary_topic):
        """
        Analyze how the primary topic relates to emotions
        """
        context_analysis = {
            'topic_emotion_relationship': 'neutral',
            'stress_level': 'low',
            'support_needed': 'general'
        }
        
        # Analyze stress indicators
        stress_words = ['stress', 'overwhelmed', 'pressure', 'anxious', 'worried', 'concerned']
        stress_count = sum(1 for word in stress_words if word in text_lower)
        
        if stress_count > 2:
            context_analysis['stress_level'] = 'high'
        elif stress_count > 0:
            context_analysis['stress_level'] = 'moderate'
        
        # Analyze topic-emotion relationships
        if primary_topic == 'work' and stress_count > 0:
            context_analysis['topic_emotion_relationship'] = 'stressful'
            context_analysis['support_needed'] = 'stress_management'
        elif primary_topic == 'relationships' and any(word in text_lower for word in ['sad', 'angry', 'hurt']):
            context_analysis['topic_emotion_relationship'] = 'conflict'
            context_analysis['support_needed'] = 'relationship_support'
        elif primary_topic == 'health' and any(word in text_lower for word in ['worried', 'scared', 'anxious']):
            context_analysis['topic_emotion_relationship'] = 'health_anxiety'
            context_analysis['support_needed'] = 'health_support'
        
        return context_analysis
    
    def _combine_analysis(self, vader_scores, emotion_scores, crisis_level, context_info, linguistic_patterns):
        """
        Combine all analyses into a comprehensive understanding
        """
        # Determine primary emotion
        primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0] if emotion_scores else 'neutral'
        
        # Determine emotional intensity
        intensity = self._determine_intensity(vader_scores, emotion_scores, linguistic_patterns)
        
        # Determine support strategy
        support_strategy = self._determine_support_strategy(
            primary_emotion, intensity, crisis_level, context_info
        )
        
        # Determine emotional complexity
        emotional_complexity = self._assess_emotional_complexity(emotion_scores, linguistic_patterns)
        
        return {
            'primary_emotion': primary_emotion,
            'intensity': intensity,
            'support_strategy': support_strategy,
            'emotional_complexity': emotional_complexity,
            'emotional_state': self._summarize_emotional_state(primary_emotion, intensity, crisis_level)
        }
    
    def _determine_intensity(self, vader_scores, emotion_scores, linguistic_patterns):
        """
        Determine the overall emotional intensity
        """
        # Base intensity from VADER
        vader_intensity = abs(vader_scores['compound'])
        
        # Adjust based on emotion scores
        max_emotion_score = max(emotion_scores.values()) if emotion_scores else 0
        emotion_intensity = min(max_emotion_score / 3, 1.0)  # Normalize to 0-1
        
        # Adjust based on linguistic patterns
        pattern_intensity = linguistic_patterns.get('intensity', 0)
        
        # Combine all intensity indicators
        combined_intensity = (vader_intensity + emotion_intensity + pattern_intensity) / 3
        
        if combined_intensity > 0.7:
            return 'high'
        elif combined_intensity > 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _determine_support_strategy(self, primary_emotion, intensity, crisis_level, context_info):
        """
        Determine the best support strategy based on analysis
        """
        if crisis_level['needs_immediate_attention']:
            return 'crisis_intervention'
        
        if primary_emotion in ['sadness', 'fear'] and intensity == 'high':
            return 'emotional_support'
        elif primary_emotion in ['anger', 'disgust'] and intensity == 'high':
            return 'de_escalation'
        elif primary_emotion in ['joy', 'trust', 'excitement']:
            return 'positive_reinforcement'
        elif context_info.get('stress_level') == 'high':  # Use .get() with default
            return 'stress_management'
        else:
            return 'exploration'
    
    def _assess_emotional_complexity(self, emotion_scores, linguistic_patterns):
        """
        Assess how complex the emotional state is
        """
        # Count emotions with significant scores
        significant_emotions = sum(1 for score in emotion_scores.values() if score > 0.5)
        
        # Check for mixed emotions
        mixed_emotions = sum(1 for score in emotion_scores.values() if 0.1 < score < 2)
        
        if significant_emotions > 3 or mixed_emotions > 4:
            return 'complex'
        elif significant_emotions > 1 or mixed_emotions > 2:
            return 'moderate'
        else:
            return 'simple'
    
    def _summarize_emotional_state(self, primary_emotion, intensity, crisis_level):
        """
        Create a human-readable summary of the emotional state
        """
        if crisis_level['needs_immediate_attention']:
            return f"Critical emotional crisis requiring immediate attention"
        
        intensity_desc = "very " if intensity == 'high' else "moderately " if intensity == 'medium' else ""
        return f"{intensity_desc}{primary_emotion} emotional state"
    
    def _calculate_confidence(self, vader_scores, emotion_scores, linguistic_patterns):
        """
        Calculate confidence in our emotional analysis
        """
        # VADER confidence
        vader_confidence = abs(vader_scores['compound'])
        
        # Emotion detection confidence
        max_emotion = max(emotion_scores.values()) if emotion_scores else 0
        emotion_confidence = min(max_emotion / 3, 1.0)
        
        # Linguistic pattern confidence
        pattern_confidence = sum(linguistic_patterns.values()) / len(linguistic_patterns) if linguistic_patterns else 0
        
        # Overall confidence
        overall_confidence = (vader_confidence + emotion_confidence + pattern_confidence) / 3
        
        return {
            'overall': overall_confidence,
            'vader': vader_confidence,
            'emotion_detection': emotion_confidence,
            'linguistic_patterns': pattern_confidence
        }
    
    def _load_emotion_keywords(self):
        """
        Load emotion-specific keywords for analysis
        """
        return {
            'joy': ['happy', 'excited', 'thrilled', 'joy', 'delighted', 'wonderful', 'amazing', 'great', 'fantastic', 'awesome'],
            'sadness': ['sad', 'depressed', 'down', 'hopeless', 'lonely', 'miserable', 'unhappy', 'grief', 'sorrow', 'melancholy'],
            'anger': ['angry', 'mad', 'furious', 'irritated', 'annoyed', 'frustrated', 'rage', 'hate', 'livid', 'enraged'],
            'fear': ['afraid', 'scared', 'terrified', 'anxious', 'worried', 'nervous', 'panic', 'dread', 'frightened', 'alarmed'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned', 'unexpected', 'startled', 'bewildered'],
            'disgust': ['disgusted', 'revolted', 'appalled', 'sickened', 'repulsed', 'horrified', 'nauseated'],
            'trust': ['trust', 'confident', 'secure', 'safe', 'reliable', 'dependable', 'assured', 'certain'],
            'anticipation': ['excited', 'eager', 'hopeful', 'optimistic', 'looking forward', 'anticipating', 'expectant'],
            'love': ['love', 'adore', 'cherish', 'care', 'affection', 'fondness', 'devotion'],
            'confusion': ['confused', 'puzzled', 'perplexed', 'baffled', 'uncertain', 'unsure', 'doubtful'],
            'excitement': ['excited', 'thrilled', 'pumped', 'energized', 'enthusiastic', 'motivated'],
            'worry': ['worried', 'concerned', 'anxious', 'nervous', 'uneasy', 'troubled']
        }
    
    def _load_crisis_keywords(self):
        """
        Load crisis-indicating keywords
        """
        return [
            'suicide', 'kill myself', 'want to die', 'end it all', 'no reason to live',
            'everyone would be better off', 'can\'t take it anymore', 'give up',
            'nothing matters', 'hopeless', 'worthless', 'useless', 'no point',
            'better off dead', 'don\'t want to live', 'end my life'
        ]
    
    def _load_intensity_modifiers(self):
        """
        Load words that modify emotional intensity
        """
        return {
            'intensifiers': ['very', 'really', 'extremely', 'incredibly', 'absolutely', 'totally', 'completely'],
            'deintensifiers': ['slightly', 'kind of', 'sort of', 'a little', 'somewhat', 'moderately', 'reasonably']
        }
    
    def _empty_analysis(self):
        """
        Return empty analysis structure for invalid input
        """
        return {
            'basic_sentiment': {'pos': 0, 'neg': 0, 'neu': 1, 'compound': 0},
            'emotions': {},
            'crisis_level': {'level': 0, 'indicators': [], 'needs_immediate_attention': False, 'risk_category': 'none'},
            'context': {'topics': {}, 'primary_topic': 'general', 'emotional_context': {}},
            'linguistic_patterns': {},
            'overall_analysis': {'primary_emotion': 'neutral', 'intensity': 'low', 'support_strategy': 'exploration', 'emotional_complexity': 'simple', 'emotional_state': 'neutral emotional state'},
            'confidence': {'overall': 0, 'vader': 0, 'emotion_detection': 0, 'linguistic_patterns': 0}
        } 