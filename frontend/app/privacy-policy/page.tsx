export default function PrivacyPolicy() {
    return (
        <main className="min-h-screen p-12 text-white bg-[#0a192f]">
            <div className="max-w-3xl mx-auto">
                <h1 className="text-3xl font-bold mb-4">Privacy Policy</h1>
                <p className="mb-4">
                    We respect your privacy. VibeRadar does not collect personal data beyond what is necessary for the app to function and for us to do basic analytics.
                </p>

                <p className="mb-4">
                    For analytics, we use PostHog, an open-source analytics tool. It helps us understand how users interact with our website. We have configured PostHog to avoid the use of cookies and to prevent the collection of any personal data.
                </p>

                <p className="mb-4">
                    The drawn arcs on the globe are stored temporarily on our server to allow others to get inspired. It is not linked to any personal information and deleted after a short period.
                </p>

                <p className="text-sm text-gray-400 mt-6">
                    If you have questions, feel free to contact us at hello@viberadar.io.
                </p>
            </div>
        </main>
    );
}
