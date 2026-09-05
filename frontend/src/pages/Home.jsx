import { CalendarDays, MapPin, Trophy, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#FFFFF0] text-slate-900">

      {/* Hero Section */}
      <section className="flex min-h-screen items-center justify-center px-6">
        <div className="max-w-7xl text-center">

          <p className="mb-4 text-lg text-red-400 tracking-widest uppercase">
            IIIT UNA Presents
          </p>

          <h1 className="text-6xl font-extrabold md:text-8xl">
            MRIDANG
          </h1>

          <p className="mt-4 text-2xl text-gray-300">
            Annual Cultural Festival
          </p>

          <p className="mx-auto mt-8 max-w-3xl text-lg leading-8 text-gray-400">
            Experience three unforgettable days filled with music, dance,
            drama, gaming, competitions, workshops, and endless memories.
          </p>

          <div className="mt-10 flex flex-wrap justify-center gap-6">

            <div className="flex items-center gap-2 rounded-lg bg-slate-900 px-5 py-3">
              <CalendarDays className="text-red-500" />
              20–22 March 2027
            </div>

            <div className="flex items-center gap-2 rounded-lg bg-slate-900 px-5 py-3">
              <MapPin className="text-red-500" />
              IIIT Una
            </div>

          </div>

          <div className="mt-12 flex justify-center gap-5">

            <button className="rounded-lg bg-red-600 px-8 py-4 font-semibold transition hover:bg-red-700">
              Register Now
            </button>

            <button className="flex items-center gap-2 rounded-lg border border-gray-600 px-8 py-4 hover:bg-slate-900">
              Explore Events
              <ArrowRight size={18} />
            </button>

          </div>

        </div>
      </section>

      {/* Highlights */}
      <section className="px-6 py-24">
        <div className="mx-auto max-w-7xl">

          <h2 className="mb-12 text-center text-4xl font-bold">
            Fest Highlights
          </h2>

          <div className="grid gap-8 md:grid-cols-4">

            <div className="rounded-xl bg-slate-900 p-8 text-center">
              <h3 className="text-5xl font-bold text-red-500">50+</h3>
              <p className="mt-3 text-gray-400">Events</p>
            </div>

            <div className="rounded-xl bg-slate-900 p-8 text-center">
              <h3 className="text-5xl font-bold text-red-500">3000+</h3>
              <p className="mt-3 text-gray-400">Participants</p>
            </div>

            <div className="rounded-xl bg-slate-900 p-8 text-center">
              <h3 className="text-5xl font-bold text-red-500">₹5L+</h3>
              <p className="mt-3 text-gray-400">Prize Pool</p>
            </div>

            <div className="rounded-xl bg-slate-900 p-8 text-center">
              <Trophy className="mx-auto mb-4 text-yellow-400" size={40} />
              <p className="text-gray-400">National Level Competitions</p>
            </div>

          </div>

        </div>
      </section>

      {/* Featured Events */}
      <section className="px-6 py-20 bg-slate-900">

        <div className="mx-auto max-w-7xl">

          <h2 className="mb-12 text-center text-4xl font-bold">
            Featured Events
          </h2>

          <div className="grid gap-8 md:grid-cols-3">

            {[
              "Hackathon",
              "Battle of Bands",
              "BGMI Tournament",
            ].map((event) => (
              <div
                key={event}
                className="rounded-xl border border-slate-700 p-8 transition hover:border-red-500"
              >
                <div className="mb-6 h-48 rounded-lg bg-slate-800"></div>

                <h3 className="text-2xl font-bold">
                  {event}
                </h3>

                <p className="mt-3 text-gray-400">
                  Placeholder description for the event.
                </p>

                <button className="mt-6 text-red-400 hover:text-red-500">
                  Learn More →
                </button>

              </div>
            ))}

          </div>

        </div>

      </section>

      {/* CTA */}
      <section className="px-6 py-24 text-center">

        <h2 className="text-5xl font-bold">
          Ready to be a Part of MRIDANG?
        </h2>

        <p className="mx-auto mt-6 max-w-2xl text-gray-400">
          Join hundreds of students from across the country and celebrate
          creativity, talent, and innovation.
        </p>

        <button className="mt-10 rounded-lg bg-red-600 px-10 py-4 text-lg font-semibold hover:bg-red-700">
          Register Now
        </button>

      </section>

    </main>
  );
}