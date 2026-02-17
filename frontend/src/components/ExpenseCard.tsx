// یک Interface تعریف می‌کنیم تا ساختار داده مشخص باشد
interface ExpenseProps {
  title: string;
  amount: number;
  category: string;
}

export default function ExpenseCard({ title, amount, category }: ExpenseProps) {
  return (
    <div className="flex justify-between p-4 bg-white shadow-sm rounded-xl mb-2 border border-gray-100">
      <div>
        <p className="font-bold text-gray-800">{title}</p>
        <p className="text-sm text-gray-500">{category}</p>
      </div>
      <p className="font-semibold text-red-500">€{amount.toFixed(2)}</p>
    </div>
  );
}