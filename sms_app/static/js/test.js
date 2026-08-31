// ====================================================================
// NRIIT SMS - Python FullStack Curriculum Logic & Algorithmic Concepts
// ====================================================================
console.log("=== NRIIT Python FullStack Programming Logics & Algorithms ===");

// --------------------------------------------------------------------
// 1. PYTHON CURRICULUM MODULE TRACKER (Dictionary / Object equivalent)
// --------------------------------------------------------------------
// In Python: course_modules = {"Python Core": True, "Flask & Django": True, ...}
const pythonFullStackModules = [
  { module: "Python Core & OOPs", completed: true, score: 92 },
  { module: "Flask & Django REST Framework", completed: true, score: 88 },
  { module: "SQL, PostgreSQL & SQLAlchemy", completed: true, score: 95 },
  { module: "HTML, CSS, JavaScript & Bootstrap", completed: true, score: 90 },
  { module: "Capstone Industry Project", completed: false, score: 0 }
];

const completedModules = pythonFullStackModules.filter(m => m.completed);
const pendingModules = pythonFullStackModules.filter(m => !m.completed);

console.log("\n--- Python FullStack Module Progress ---");
console.log(`Completed Modules (${completedModules.length}):`, completedModules.map(m => m.module));
console.log(`Pending Modules (${pendingModules.length}):`, pendingModules.map(m => m.module));

// --------------------------------------------------------------------
// 2. PALINDROME CHECKER LOGIC (Python String Processing Challenge)
// --------------------------------------------------------------------
// In Python: is_palindrome = lambda s: s == s[::-1]
function isPalindrome(str) {
  const cleanedStr = str.toLowerCase().replace(/[^a-z0-9]/g, "");
  const reversedStr = cleanedStr.split("").reverse().join("");
  return cleanedStr === reversedStr;
}

const testStrings = ["racecar", "python", "level", "nriit"];
console.log("\n--- Python Algorithm Challenge: Palindrome Checker ---");
testStrings.forEach(word => {
  console.log(`Word "${word}" is Palindrome? -> ${isPalindrome(word) ? "YES" : "NO"}`);
});

// --------------------------------------------------------------------
// 3. FIBONACCI SERIES GENERATOR (Python Recursive / Iterative Logic)
// --------------------------------------------------------------------
// In Python:
// def fibonacci(n):
//     a, b = 0, 1
//     for _ in range(n):
//         yield a
//         a, b = b, a + b
function generateFibonacci(n) {
  const series = [];
  let a = 0, b = 1;
  for (let i = 0; i < n; i++) {
    series.push(a);
    const next = a + b;
    a = b;
    b = next;
  }
  return series;
}

console.log("\n--- Python Algorithm Challenge: First 10 Fibonacci Numbers ---");
console.log(generateFibonacci(10));


const studentMarks = [75, 82, 90, 67, 88, 93, 80, 55, 96];

const evenScores = studentMarks.filter(mark => mark % 2 === 0);
const oddScores = studentMarks.filter(mark => mark % 2 !== 0);

console.log("\n--- Python List Comprehension Style Filtering ---");
console.log("All Scores:", studentMarks);
console.log("Even Scores:", evenScores);
console.log("Odd Scores:", oddScores);

// --------------------------------------------------------------------
// 5. FACTORIAL CALCULATOR LOGIC
// --------------------------------------------------------------------

function calculateFactorial(num) {
  if (num < 0) return -1;
  if (num === 0 || num === 1) return 1;
  let result = 1;
  for (let i = 2; i <= num; i++) {
    result *= i;
  }
  return result;
}

console.log("\n--- Python Math Logic: Factorial Calculation ---");
console.log(`Factorial of 5 (5!): ${calculateFactorial(5)}`);
console.log(`Factorial of 6 (6!): ${calculateFactorial(6)}`);
