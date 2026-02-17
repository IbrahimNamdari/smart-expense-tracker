'use client';
import { useEffect, useState } from 'react';
import { getExpenses, addExpenseAI, getSummary } from '@/lib/api';
import ExpenseCard from '@/components/ExpenseCard';
import ExpenseChart from '@/components/ExpenseChart';

interface Expense {
  id: number;
  title: string;
  amount: number;
  category: string;
  date: string;
}

interface SummaryData {
  [key: string]: number;
}

export default function Home() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [summary, setSummary] = useState<SummaryData>({});
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    try {
      const resExp = await getExpenses();
      const resSum = await getSummary();
      setExpenses(resExp.data);
      setSummary(resSum.data);
    } catch (error) {
      console.error("Failed to fetch data", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAISubmit = async () => {
    if (!inputText) return;
    setLoading(true);
    try {
      await addExpenseAI(inputText);
      setInputText("");
      await fetchData();
    } catch (error) {
      console.error("AI processing failed", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-md mx-auto p-6 bg-gray-50 min-h-screen">
      <h1 className="text-2xl font-bold mb-2">Guten Tag, Alexander!</h1>
      <p className="text-gray-500 mb-6">Total Balance: <span className="text-black font-bold">€2,450.00</span></p>

      {Object.keys(summary).length > 0 && <ExpenseChart data={summary} />}

      <div className="bg-blue-600 p-6 rounded-3xl text-white mb-8 shadow-lg">
        <h2 className="font-semibold mb-4 text-center text-blue-100">Magic AI Input ✨</h2>
        <input 
          className="w-full p-3 rounded-xl text-black outline-none focus:ring-2 focus:ring-blue-300"
          placeholder="e.g. 50€ for Groceries"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <button 
          onClick={handleAISubmit}
          disabled={loading}
          className="w-full mt-3 bg-white text-blue-600 font-bold py-3 rounded-xl hover:bg-gray-100 transition disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Process with Gemini 2.0"}
        </button>
      </div>

      <h3 className="text-lg font-bold mb-4">Recent Activity</h3>
      <div className="space-y-2">
        {expenses.map((exp: Expense) => (
          <ExpenseCard key={exp.id} {...exp} />
        ))}
      </div>
    </main>
  );
}