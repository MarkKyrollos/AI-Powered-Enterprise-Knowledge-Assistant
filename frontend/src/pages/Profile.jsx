import React from "react";
import Layout from "../components/Layout";
import { useAuth } from "../contexts/AuthContext";

export default function Profile() {
  const { user } = useAuth();

  return (
    <Layout>
      <div className="mx-auto max-w-2xl px-8 py-10">
        <h1 className="text-2xl font-semibold tracking-tight">Profile</h1>
        <div className="card mt-6 divide-y divide-ink/10">
          <div className="flex items-center justify-between px-5 py-4">
            <span className="text-sm text-ink/50">Email</span>
            <span className="text-sm font-medium">{user?.email}</span>
          </div>
          <div className="flex items-center justify-between px-5 py-4">
            <span className="text-sm text-ink/50">Member since</span>
            <span className="text-sm font-medium">
              {user?.created_at ? new Date(user.created_at).toLocaleDateString() : "-"}
            </span>
          </div>
          <div className="flex items-center justify-between px-5 py-4">
            <span className="text-sm text-ink/50">User ID</span>
            <span className="text-sm font-medium">#{user?.id}</span>
          </div>
        </div>
      </div>
    </Layout>
  );
}
