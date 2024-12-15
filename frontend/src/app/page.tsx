"use client";
import Visualization from "./Visualization";

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

      <div className="flex justify-center gap-8 p-8">
        <div className="flex flex-col gap-8">
          <div className="rounded-lg p-4 w-full ">
            <Visualization
              id="viz1734229567691"
              name="VOO_price_and_volume/PriceandVolume"
              staticImageUrl="https://public.tableau.com/static/images/VO/VOO_price_and_volume/PriceandVolume/1_rss.png"
            />
          </div>
        </div>

        <div className="flex flex-col justify-center gap-8">
          <div className="text-left">
            <h2 className="text-4xl font-bold">
              Conclusions Based on Data Visualization
            </h2>
          </div>
        </div>
      </div>
    </div>
  );
}
