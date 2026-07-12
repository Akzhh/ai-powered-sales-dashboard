import { EXPORT_EXCEL_URL, EXPORT_PDF_URL } from '../api';

export default function TopNav({ title, description }) {
  return (
    <header className="top-nav">
      <div className="page-title">
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      <div className="export-actions">
        <a
          href={EXPORT_EXCEL_URL}
          className="btn-export btn-excel"
          id="export-excel-link"
          download
        >
          <i className="fa-solid fa-file-excel" />
          Export Excel
        </a>
        <a
          href={EXPORT_PDF_URL}
          className="btn-export btn-pdf"
          id="export-pdf-link"
          download
        >
          <i className="fa-solid fa-file-pdf" />
          PDF Report
        </a>
      </div>
    </header>
  );
}
