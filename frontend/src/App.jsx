import { useState, useEffect } from 'react'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default function App() {
  const [url, setUrl] = useState('')
  const [imageFile, setImageFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [stats, setStats] = useState(null)
  const [page, setPage] = useState('home') // advanced settings home page contacts maybe

  useEffect(() => {
    fetch(`${BACKEND_URL}/stats`)
      .then(r => r.json())
      .then(setStats)
      .catch(() => {})
  }, [])

  function handleImageChange(e) {
    const file = e.target.files[0]
    if (!file) return
    setImageFile(file)
    setImagePreview(URL.createObjectURL(file))
  }

  async function handleConvert() {
    if (!url.trim()) return
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const formData = new FormData()
      formData.append('url', url)
      if (imageFile) formData.append('image', imageFile)

      const res = await fetch(`${BACKEND_URL}/convert`, {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || 'Conversion failed.')
      }

      const filename = decodeURIComponent(res.headers.get('X-Filename') || 'audio.mp3')
      const blob = await res.blob()
      const downloadUrl = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = downloadUrl
      a.download = filename
      a.click()
      window.URL.revokeObjectURL(downloadUrl)
      setSuccess(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center px-4">
    
      <div className="fixed top-0 w-full flex gap-10 justify-end items-center text-lg px-6 py-4 text-gray-350">
        <button>Home</button>
        <button>Advanced</button>
        <button>About</button>
        <button>Contact</button>
      </div>

      {/* Header */}
      <h1 className="text-8xl font-bold mb-9">YT2MP3</h1>
      <p className="text-lg text-gray-400 mb-9">Paste a YouTube URL and download it as MP3.</p>
      {/* Input + Button */}
      <div className="flex flex-col sm:flex-row gap-3 w-full max-w-2xl">
        <input
          type="text"
          placeholder="https://www.youtube.com/watch?v=..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="flex-1 rounded-lg bg-gray-800 border border-gray-700 px-5 py-4 text-base outline-none focus:border-indigo-500 transition"
        />
        <button
          onClick={handleConvert}
          disabled={loading || !url.trim()}
          className="rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed px-7 py-4 text-base font-semibold transition"
        >
          {loading ? 'Converting...' : 'Convert'}
        </button>
      </div>

      {/* Album art upload */}
      <div className="mt-5 w-full max-w-2xl">
        <label className="flex items-center gap-4 cursor-pointer group">
          {imagePreview ? (
            <img src={imagePreview} alt="Album art preview" className="w-20 h-20 rounded-lg object-cover border border-gray-700" />
          ) : (
            <div className="w-20 h-20 rounded-lg bg-gray-800 border border-dashed border-gray-700 flex items-center justify-center text-gray-500 text-sm group-hover:border-indigo-500 transition">
              Art
            </div>
          )}
          <div>
            <p className="text-base text-gray-300">{imageFile ? imageFile.name : 'Attach album art (optional)'}</p>
            <p className="text-sm text-gray-500">Click to choose an image</p>
          </div>
          <input type="file" accept="image/*" onChange={handleImageChange} className="hidden" />
        </label>
      </div>

      {/* Stats */}
      {stats?.count > 0 && (
        <p className="absolute bottom-10 text-s text-gray-500">
          {stats.count.toLocaleString()} songs converted since {new Date(stats.since).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
        </p>
      )}

      {/* Feedback */}
      {error && (
        <p className="mt-4 text-red-400 text-sm">{error}</p>
      )}
      {success && (
        <p className="mt-4 text-green-400 text-sm">Download started!</p>
      )}
    </div>
  )
}
