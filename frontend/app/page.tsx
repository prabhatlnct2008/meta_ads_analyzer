import Link from 'next/link';
import { Button } from '@/components/ui/Button';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          <div className="text-2xl font-bold text-blue-600">Meta Ads Analyzer</div>
          <div className="space-x-4">
            <Link href="/login">
              <Button variant="outline" size="sm">Login</Button>
            </Link>
            <Link href="/signup">
              <Button size="sm">Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20 text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
          Understand Your Facebook Ads<br />
          <span className="text-blue-600">in Plain English</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Connect your Meta Ads account and get clear, AI-powered insights on what&apos;s working,
          what&apos;s wasting money, and what to do next.
        </p>
        <div className="flex justify-center gap-4">
          <Link href="/signup">
            <Button size="lg">Connect Your Facebook Ads Account</Button>
          </Link>
          <Button variant="outline" size="lg">Watch Demo</Button>
        </div>

        {/* Mock Dashboard Preview */}
        <div className="mt-16 bg-white rounded-lg shadow-2xl p-8 max-w-4xl mx-auto border border-gray-200">
          <div className="bg-gradient-to-r from-blue-100 to-purple-100 rounded-lg p-6">
            <p className="text-left text-gray-800 italic">
              &quot;Your CPA increased 23% last week because mobile placements stopped performing.
              Consider testing new creatives for Instagram Feed.&quot;
            </p>
            <p className="text-right text-sm text-gray-600 mt-2">— AI Assistant</p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Connect</h3>
              <p className="text-gray-600">
                Securely connect your Facebook / Meta Ads account in a few clicks using official Meta login.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Ask</h3>
              <p className="text-gray-600">
                Ask questions like &quot;Which campaigns should I pause?&quot; or &quot;Why did my ROAS drop last week?&quot;
              </p>
            </div>
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Act</h3>
              <p className="text-gray-600">
                Get simple explanations, key numbers, and clear recommendations you can implement right away.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-20">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">Why Choose Us</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-lg shadow-md">
              <div className="text-3xl mb-4">📊</div>
              <h3 className="text-xl font-semibold mb-2">Know What&apos;s Working</h3>
              <p className="text-gray-600">
                See your top campaigns, ad sets, and ads by ROAS, CPA, CTR and more—without
                digging through endless reports.
              </p>
            </div>
            <div className="bg-white p-8 rounded-lg shadow-md">
              <div className="text-3xl mb-4">💰</div>
              <h3 className="text-xl font-semibold mb-2">Spot Wasted Spend</h3>
              <p className="text-gray-600">
                Instantly identify under-performing campaigns and placements that are burning budget.
              </p>
            </div>
            <div className="bg-white p-8 rounded-lg shadow-md">
              <div className="text-3xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold mb-2">AI-Powered Answers</h3>
              <p className="text-gray-600">
                Don&apos;t guess. Ask the built-in AI assistant and get explanations you actually understand.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">Features</h2>
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            <div className="flex items-start">
              <span className="text-blue-600 mr-3">✓</span>
              <span>Connect multiple Meta ad accounts</span>
            </div>
            <div className="flex items-start">
              <span className="text-blue-600 mr-3">✓</span>
              <span>Overview dashboard with spend, conversions, ROAS</span>
            </div>
            <div className="flex items-start">
              <span className="text-blue-600 mr-3">✓</span>
              <span>Campaign / adset / ad breakdowns</span>
            </div>
            <div className="flex items-start">
              <span className="text-blue-600 mr-3">✓</span>
              <span>AI chat for performance questions</span>
            </div>
            <div className="flex items-start">
              <span className="text-blue-600 mr-3">✓</span>
              <span>Simple recommendations for pausing, scaling, and testing</span>
            </div>
            <div className="flex items-start">
              <span className="text-blue-600 mr-3">✓</span>
              <span>Secure Meta OAuth login; revoke access anytime</span>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-20">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">What Our Users Say</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <p className="text-gray-600 italic mb-4">
                &quot;I finally understand where my ad money goes. The AI chat explains it like I&apos;m five.&quot;
              </p>
              <p className="font-semibold">Sarah Johnson</p>
              <p className="text-sm text-gray-500">Small Business Owner</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <p className="text-gray-600 italic mb-4">
                &quot;This tool saved me hours every week. I can see what&apos;s working at a glance.&quot;
              </p>
              <p className="font-semibold">Michael Chen</p>
              <p className="text-sm text-gray-500">Marketing Manager</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <p className="text-gray-600 italic mb-4">
                &quot;The recommendations are spot-on. We&apos;ve improved our ROAS by 40%.&quot;
              </p>
              <p className="font-semibold">Emily Davis</p>
              <p className="text-sm text-gray-500">E-commerce Founder</p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">Simple Pricing</h2>
          <div className="max-w-md mx-auto bg-gradient-to-br from-blue-50 to-purple-50 p-8 rounded-lg shadow-lg border-2 border-blue-200">
            <h3 className="text-2xl font-bold mb-2">Starter Plan</h3>
            <p className="text-gray-600 mb-6">Perfect for small businesses</p>
            <p className="text-4xl font-bold mb-6">
              <span className="text-blue-600">Early Access</span>
            </p>
            <p className="text-gray-600 mb-6">Limited slots available</p>
            <Link href="/signup">
              <Button size="lg" className="w-full">Join Early Access</Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-4">Ready to stop guessing your Facebook ad performance?</h2>
          <p className="text-xl mb-8">
            Connect your Meta Ads account and get your first AI-generated performance breakdown in minutes.
          </p>
          <Link href="/signup">
            <Button size="lg" variant="outline" className="bg-white text-blue-600 hover:bg-gray-100">
              Get Started – Connect Ads Account
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="container mx-auto px-6 text-center">
          <p>&copy; 2024 Meta Ads Analyzer. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
