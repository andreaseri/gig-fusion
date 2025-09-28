import React from 'react'

export default function InfoTile({ band, location, price_eur, status_kind }: { band?: string; location?: string; price_eur?: number | string; status_kind?: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', width: '100%', height: 64 }}>
      <div style={{ flex: 1, overflow: 'hidden' }}>
        <div style={{ fontSize: 16, fontWeight: 800, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{band ?? ''}</div>
        <div style={{ fontSize: 14, color: '#333', marginTop: 2, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{location ?? ''}</div>
        <div style={{ fontSize: 12, color: '#666', marginTop: 6, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{status_kind ?? ''}</div>
      </div>
      <div style={{ marginLeft: 12, minWidth: 72, textAlign: 'right', fontWeight: 700 }}>{price_eur != null && price_eur !== '' ? `€${price_eur}` : ''}</div>
    </div>
  )
}
