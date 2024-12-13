export default function Home() {
  return (
    <div className="bg-primaryDark min-h-screen text-primaryLight flex flex-col text-center pt-10">
      <h1 className="text-6xl font-extrabold">Comparing Two ETFs</h1>
      <div className="flex-row flex justify-center text-4xl gap-8 pt-6 font-bold">
        <div className="border-2 border-primaryAccent rounded-3xl px-10 py-1">
          SPY
        </div>
        <div>vs</div>
        <div className="border-2 border-primaryAccent rounded-3xl px-10 py-1">
          VOO
        </div>
      </div>
      <div className="border-b border-primaryAccent w-3/5 mx-auto pt-10"></div>

      <div>main body goes here</div>
    </div>
  );
}
