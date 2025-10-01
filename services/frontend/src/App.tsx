import Search from './components/Search'

function App() {
  return (
    <div className="p-6">
      <div className="w-full max-w-[1200px] mx-auto">
        <div className="grid grid-cols-[1fr_auto] gap-4 items-start mb-4">
          <h1 className="text-4xl font-extrabold tracking-tight">gigfusion</h1>
          <div className="col-span-2">
            <Search />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
