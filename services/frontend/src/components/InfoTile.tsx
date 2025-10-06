
function InfoTile({ band, location, price_eur, status_kind, status_raw }: { band?: string; location?: string; price_eur?: number | string; status_kind?: string; status_raw?: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', width: '100%', height: 64 }}>
      <div style={{ flex: 1, overflow: 'hidden' }}>
        <div style={{ fontSize: 16, fontWeight: 800, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{band ?? ''}</div>
        <div style={{ fontSize: 14, color: 'var(--text)', marginTop: 2, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{location ?? ''}</div>
        <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 6, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{status_kind === 'verlegt' ? status_raw : (status_kind ?? '')}</div>
      </div>
      <div style={{ marginLeft: 12, minWidth: 72, textAlign: 'right', fontWeight: 700 }}>{price_eur != null && price_eur !== '' ? `€${price_eur}` : ''}</div>
    </div>
  )
}

export default InfoTile;