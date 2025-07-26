from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import Category, Bin, Card, QuizAttempt, QuizAnswer


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_category_creation(self):
        """Test category creation with valid data"""
        self.assertEqual(self.category.name, "Test Category")
        self.assertIsNotNone(self.category.created_at)
        self.assertIsNotNone(self.category.updated_at)

    def test_category_string_representation(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), "Test Category")

    def test_category_unique_name(self):
        """Test that category names must be unique"""
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Test Category")

    def test_category_update_timestamp(self):
        """Test that updated_at changes when category is updated"""
        original_updated_at = self.category.updated_at
        self.category.name = "Updated Category"
        self.category.save()
        self.assertGreater(self.category.updated_at, original_updated_at)


class BinModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.bin = Bin.objects.create(category=self.category, name="Test Bin")

    def test_bin_creation(self):
        """Test bin creation with valid data"""
        self.assertEqual(self.bin.name, "Test Bin")
        self.assertEqual(self.bin.category, self.category)
        self.assertIsNotNone(self.bin.created_at)

    def test_bin_string_representation(self):
        """Test bin string representation"""
        expected_str = f"{self.category.name} - {self.bin.name}"
        self.assertEqual(str(self.bin), expected_str)

    def test_bin_unique_together(self):
        """Test that bin names must be unique within a category"""
        with self.assertRaises(IntegrityError):
            Bin.objects.create(category=self.category, name="Test Bin")

    def test_bin_same_name_different_category(self):
        """Test that same bin name can exist in different categories"""
        other_category = Category.objects.create(name="Other Category")
        other_bin = Bin.objects.create(category=other_category, name="Test Bin")
        self.assertNotEqual(self.bin.id, other_bin.id)

    def test_bin_cascade_delete(self):
        """Test that bins are deleted when category is deleted"""
        category_id = self.category.id
        bin_id = self.bin.id
        self.category.delete()
        
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category_id)
        with self.assertRaises(Bin.DoesNotExist):
            Bin.objects.get(id=bin_id)


class CardModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.correct_bin = Bin.objects.create(category=self.category, name="Correct Bin")
        self.card = Card.objects.create(
            category=self.category,
            text="Test question?",
            correct_bin=self.correct_bin
        )

    def test_card_creation(self):
        """Test card creation with valid data"""
        self.assertEqual(self.card.text, "Test question?")
        self.assertEqual(self.card.category, self.category)
        self.assertEqual(self.card.correct_bin, self.correct_bin)
        self.assertIsNotNone(self.card.created_at)
        self.assertIsNotNone(self.card.updated_at)

    def test_card_string_representation(self):
        """Test card string representation"""
        expected_str = "Test question?..."
        self.assertEqual(str(self.card), expected_str)

    def test_card_long_text_string_representation(self):
        """Test card string representation with long text"""
        long_text = "This is a very long question that exceeds fifty characters for testing purposes"
        long_card = Card.objects.create(
            category=self.category,
            text=long_text,
            correct_bin=self.correct_bin
        )
        expected_str = long_text[:50] + "..."
        self.assertEqual(str(long_card), expected_str)

    def test_card_cascade_delete_category(self):
        """Test that cards are deleted when category is deleted"""
        card_id = self.card.id
        self.category.delete()
        
        with self.assertRaises(Card.DoesNotExist):
            Card.objects.get(id=card_id)

    def test_card_cascade_delete_bin(self):
        """Test that cards are deleted when correct_bin is deleted"""
        card_id = self.card.id
        self.correct_bin.delete()
        
        with self.assertRaises(Card.DoesNotExist):
            Card.objects.get(id=card_id)


class QuizAttemptModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.quiz_attempt = QuizAttempt.objects.create(
            user_name="TestUser",
            category=self.category,
            score=8,
            total_questions=10
        )

    def test_quiz_attempt_creation(self):
        """Test quiz attempt creation"""
        self.assertEqual(self.quiz_attempt.user_name, "TestUser")
        self.assertEqual(self.quiz_attempt.category, self.category)
        self.assertEqual(self.quiz_attempt.score, 8)
        self.assertEqual(self.quiz_attempt.total_questions, 10)
        self.assertIsNotNone(self.quiz_attempt.started_at)

    def test_quiz_attempt_string_representation(self):
        """Test quiz attempt string representation"""
        expected_str = f"Quiz {self.quiz_attempt.id} - Test Category - 8/10"
        self.assertEqual(str(self.quiz_attempt), expected_str)

    def test_quiz_attempt_anonymous_user(self):
        """Test quiz attempt with anonymous user"""
        anonymous_attempt = QuizAttempt.objects.create(
            category=self.category,
            score=5,
            total_questions=10
        )
        self.assertIsNone(anonymous_attempt.user_name)


class QuizAnswerModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.correct_bin = Bin.objects.create(category=self.category, name="Correct")
        self.wrong_bin = Bin.objects.create(category=self.category, name="Wrong")
        
        self.card = Card.objects.create(
            category=self.category,
            text="Test question?",
            correct_bin=self.correct_bin
        )
        
        self.quiz_attempt = QuizAttempt.objects.create(
            user_name="TestUser",
            category=self.category,
            score=1,
            total_questions=1
        )
        
        self.quiz_answer = QuizAnswer.objects.create(
            quiz_attempt=self.quiz_attempt,
            card=self.card,
            selected_bin=self.correct_bin,
            is_correct=True
        )

    def test_quiz_answer_creation(self):
        """Test quiz answer creation"""
        self.assertEqual(self.quiz_answer.quiz_attempt, self.quiz_attempt)
        self.assertEqual(self.quiz_answer.card, self.card)
        self.assertEqual(self.quiz_answer.selected_bin, self.correct_bin)
        self.assertTrue(self.quiz_answer.is_correct)
        self.assertIsNotNone(self.quiz_answer.answered_at)

    def test_quiz_answer_string_representation(self):
        """Test quiz answer string representation"""
        expected_str = f"Answer {self.quiz_answer.id} - Correct"
        self.assertEqual(str(self.quiz_answer), expected_str)

    def test_quiz_answer_wrong(self):
        """Test wrong quiz answer"""
        wrong_answer = QuizAnswer.objects.create(
            quiz_attempt=self.quiz_attempt,
            card=self.card,
            selected_bin=self.wrong_bin,
            is_correct=False
        )
        expected_str = f"Answer {wrong_answer.id} - Wrong"
        self.assertEqual(str(wrong_answer), expected_str)