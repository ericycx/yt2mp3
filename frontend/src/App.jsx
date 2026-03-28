import { useState } from 'react'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default function App() {
  const [url, setUrl] = useState('')
  const [imageFile, setImageFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

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

      {/* Header */}
      <h1 className="text-4xl font-bold mb-2">YT2MP3</h1>
      <p className="text-gray-400 mb-8">Paste a YouTube URL and download it as MP3.</p>

      {/* Input + Button */}
      <div className="flex flex-col sm:flex-row gap-3 w-full max-w-xl">
        <input
          type="text"
          placeholder="https://www.youtube.com/watch?v=..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="flex-1 rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-sm outline-none focus:border-indigo-500 transition"
        />
        <button
          onClick={handleConvert}
          disabled={loading || !url.trim()}
          className="rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 text-sm font-semibold transition"
        >
          {loading ? 'Converting...' : 'Convert'}
        </button>
      </div>

      {/* Album art upload */}
      <div className="mt-4 w-full max-w-xl">
        <label className="flex items-center gap-4 cursor-pointer group">
          {imagePreview ? (
            <img src={imagePreview} alt="Album art preview" className="w-16 h-16 rounded-lg object-cover border border-gray-700" />
          ) : (
            <div className="w-16 h-16 rounded-lg bg-gray-800 border border-dashed border-gray-700 flex items-center justify-center text-gray-500 text-xs group-hover:border-indigo-500 transition">
              Art
            </div>
          )}
          <div>
            <p className="text-sm text-gray-300">{imageFile ? imageFile.name : 'Attach album art (optional)'}</p>
            <p className="text-xs text-gray-500">Click to choose an image</p>
          </div>
          <input type="file" accept="image/*" onChange={handleImageChange} className="hidden" />
        </label>
      </div>

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
