// frontend/src/pages/NotFoundPage.tsx

import { Link } from 'react-router-dom';

const NotFoundPage = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen text-center">
      <h1 className="text-6xl font-bold text-primary">404</h1>
      <h2 className="text-2xl font-semibold mt-4">Page Not Found</h2>
      <p className="mt-2 text-gray-500">Sorry, the page you are looking for does not exist.</p>
      <Link to="/" className="mt-6 px-6 py-2 bg-primary text-white rounded-md hover:bg-primary-hover">
        Go to Dashboard
      </Link>
    </div>
  );
};

export default NotFoundPage;
