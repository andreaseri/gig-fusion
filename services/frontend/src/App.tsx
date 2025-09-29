import React from 'react'
import Search from './components/Search'
import DarkModeToggle from './components/DarkModeToggle'

export default function App(): JSX.Element{
  return (
    <div className="p-6">
      <div className="w-full max-w-[1200px] mx-auto">
        <div className="grid grid-cols-[1fr_auto] gap-4 items-start mb-4">
          <h1 className="text-4xl font-extrabold tracking-tight">gigfusion</h1>
          <DarkModeToggle />
          <div className="col-span-2">
            <Search />
          </div>
        </div>
      </div>
    </div>
  )
}
