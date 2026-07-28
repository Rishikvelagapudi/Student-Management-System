// Test JavaScript file - Arithmetic Operations & Conditional Statements
console.log("test.js loaded - LMS Calculations & Conditional Checks");

// ==========================================
// 1. ARITHMETIC OPERATIONS (LMS Fee & Score Calculations)
// ==========================================

// Course tuition fee calculation
const baseCourseFee = 15000;
const enrollmentFee = 1500;
const studyMaterialCost = 2500;

// Addition (+) & Subtraction (-)
const totalBeforeDiscount = baseCourseFee + enrollmentFee + studyMaterialCost;
const scholarshipDiscount = 3000;
const finalCourseFee = totalBeforeDiscount - scholarshipDiscount;

// Multiplication (*) & Division (/)
const monthlyInstallment = finalCourseFee / 3; // 3-month EMI plan
const totalForGroupOfFive = finalCourseFee * 5;

// Modulus (%) - checking if fee can be split evenly into 4 installments
const remainderAfterFourInstallments = finalCourseFee % 4;

console.log("=== Course Fee Calculations ===");
console.log(`Total Before Discount: ₹${totalBeforeDiscount}`);
console.log(`Final Course Fee (after ₹${scholarshipDiscount} scholarship): ₹${finalCourseFee}`);
console.log(`3-Month Installment (EMI): ₹${monthlyInstallment.toFixed(2)}`);
console.log(`Remainder after splitting into 4 installments: ₹${remainderAfterFourInstallments}`);

// Student Marks Arithmetic Calculation
const assignmentScore = 88;
const midtermScore = 92;
const finalExamScore = 85;
const totalScore = assignmentScore + midtermScore + finalExamScore;
const averagePercentage = totalScore / 3;

console.log("\n=== Student Grade Calculations ===");
console.log(`Total Score: ${totalScore}/300`);
console.log(`Average Percentage: ${averagePercentage.toFixed(2)}%`);

// ==========================================
// 2. CONDITIONAL STATEMENTS (Admission Eligibility)
// ==========================================

const age = 18;

console.log("\n=== Admission Eligibility Check ===");
if (age >= 18) {
  console.log(`Age ${age}: Eligible for admission in NRIIT Learning Management System.`);
} else {
  console.log(`Age ${age}: Not eligible for admission. Minimum age required is 18.`);
}
