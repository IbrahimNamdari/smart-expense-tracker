'use client';
import { useEffect, useState, useCallback } from 'react'; // اضافه کردن useCallback
import { getExpenses, addExpenseAI } from '@/lib/api';
import ExpenseCard from '@/components/ExpenseCard';

// تعریف تایپ برای لیست هزینه‌ها
interface Expense {
  id: number;
  title: string;
  amount: number;
  category: string;
}

export default function Home() {
  const [expenses, setExpenses] = useState<Expense[]>([]); // مشخص کردن تایپ آرایه
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);

  // استفاده از useCallback برای بهینه سازی و رفع خطای ESLint
  const fetchData = useCallback(async () => {
    try {
      const res = await getExpenses();
      setExpenses(res.data);
    } catch (error) {
      console.error("Failed to fetch expenses:", error);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]); // اضافه کردن وابستگی

  const handleAISubmit = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    try {
      await addExpenseAI(inputText);
      setInputText("");
      await fetchData();
    } catch (error) {
      console.error("AI processing failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-md mx-auto p-6 bg-gray-50 min-h-screen">
      <h1 className="text-2xl font-bold mb-2">Guten Tag, Alexander!</h1>
      {/* ... باقی کدها مثل قبل ... */}
      <div className="bg-blue-600 p-6 rounded-3xl text-white mb-8 shadow-lg">
        <h2 className="font-semibold mb-4">Magic Input ✨</h2>
        <input 
          className="w-full p-3 rounded-xl text-black shadow-inner focus:outline-none"
          placeholder="e.g. 15€ for Pizza..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <button 
          onClick={handleAISubmit}
          disabled={loading}
          className="w-full mt-3 bg-white text-blue-600 font-bold py-3 rounded-xl hover:bg-gray-100 transition disabled:bg-gray-300"
        >
          {loading ? "Processing..." : "Process with AI"}
        </button>
      </div>

      <h3 className="text-lg font-bold mb-4">Recent Activity</h3>
      {expenses.map((exp) => (
        <ExpenseCard key={exp.id} title={exp.title} amount={exp.amount} category={exp.category} />
      ))}
    </main>
  );
}